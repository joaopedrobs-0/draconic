/*
    Movimento do Draconic — efeito do KWin.

    Baseado nos efeitos "scale" e "squash" do KWin:
    SPDX-FileCopyrightText: 2018, 2021 Vlad Zahorodnii <vlad.zahorodnii@kde.org>
    Alterações para o Draconic: SPDX-FileCopyrightText: 2026 Projeto Draconic

    SPDX-License-Identifier: GPL-2.0-or-later

    Tabela "Movimento" de docs/design-system.md:

      Abrir janela      cresce de 96% e aparece      180 ms  desacelera   (reduzido: só aparece, 120 ms)
      Fechar janela     encolhe para 96% e some      140 ms  acelera      (reduzido: só some, 100 ms)
      Minimizar         encolhe em direção à dock    220 ms  suave        (reduzido: some no lugar)
      Busca e painéis   descem 8 px e aparecem       160 ms  desacelera   (reduzido: só aparece)
      Notificação       entra 16 px pela direita     200 ms  desacelera   (reduzido: só aparece)
      Menu              só opacidade                  80 ms  linear       (igual)

    As curvas do design são cubic-bezier; os efeitos do KWin só aceitam curvas
    prontas, então usamos as mais próximas:
      desacelera (0.2, 0, 0, 1)  -> OutCubic
      acelera    (0.4, 0, 1, 1)  -> InCubic
      suave      (0.4, 0, 0.2, 1)-> InOutCubic

    "Reduzir movimento" é a opção ReduzirMovimento deste efeito (kwinrc,
    grupo Effect-draconic_movimento). Use o comando draconic-reduzir-movimento.
    A velocidade de animação "Instantânea" do Plasma continua desligando tudo,
    porque todas as durações passam por animationTime().
*/

"use strict";

// Janelas que outros efeitos animam ou que não devem ter animação.
const ignorar = {
    "ksmserver ksmserver": [],
    "ksmserver-logout-greeter ksmserver-logout-greeter": [],
    "ksplashqml ksplashqml": [],
    "spectacle org.kde.spectacle": ["region-editor"],
};

const DESACELERA = QEasingCurve.OutCubic;
const ACELERA = QEasingCurve.InCubic;
const SUAVE = QEasingCurve.InOutCubic;

class MovimentoDraconic {
    constructor() {
        effect.configChanged.connect(this.lerConfig.bind(this));
        effect.animationEnded.connect(this.limparPapeis.bind(this));
        effects.windowAdded.connect(this.janelaAdicionada.bind(this));
        effects.windowClosed.connect(this.janelaFechada.bind(this));
        effects.windowDataChanged.connect(this.dadosMudaram.bind(this));
        for (const janela of effects.stackingOrder) {
            this.observarMinimizar(janela);
        }
        this.lerConfig();
    }

    lerConfig() {
        this.reduzir = effect.readConfig("ReduzirMovimento", false);
    }

    // ------------------------------------------------------------ tipos de janela
    static ignorada(janela) {
        const tags = ignorar[janela.windowClass];
        if (tags && (tags.length === 0 || tags.includes(janela.tag))) {
            return true;
        }
        return janela.lockScreen || janela.outline || janela.dndIcon || janela.tooltip;
    }

    static ehBusca(janela) {
        return janela.windowClass.indexOf("krunner") !== -1;
    }

    static ehPainel(janela) {
        // Popups dos widgets da barra (menu do sistema, bandeja, relógio...).
        return janela.appletPopup === true;
    }

    static ehNotificacao(janela) {
        return janela.notification || janela.criticalNotification;
    }

    static ehMenu(janela) {
        return janela.popupMenu || janela.dropdownMenu || janela.comboBox;
    }

    static ehJanela(janela) {
        // Mesma regra do efeito "scale": a maioria das janelas do plasmashell
        // não anima; as que têm decoração (diálogos, configurações) animam.
        if (janela.windowClass == "plasmashell plasmashell"
                || janela.windowClass == "plasmashell org.kde.plasmashell") {
            return janela.hasDecoration;
        }
        if (janela.hasDecoration) {
            return true;
        }
        if (janela.popupWindow || !janela.managed) {
            return false;
        }
        return janela.normalWindow || janela.dialog;
    }

    tipo(janela) {
        if (MovimentoDraconic.ignorada(janela)) return null;
        if (MovimentoDraconic.ehBusca(janela)) return "busca";
        if (MovimentoDraconic.ehNotificacao(janela)) return "notificacao";
        if (MovimentoDraconic.ehPainel(janela)) return "painel";
        if (MovimentoDraconic.ehMenu(janela)) return "menu";
        if (MovimentoDraconic.ehJanela(janela)) return "janela";
        return null;
    }

    // ------------------------------------------------------------ desfoque durante a animação
    forcarPapeis(janela) {
        janela.setData(Effect.WindowForceBackgroundContrastRole, true);
        janela.setData(Effect.WindowForceBlurRole, true);
    }

    limparPapeis(janela) {
        janela.setData(Effect.WindowForceBackgroundContrastRole, null);
        janela.setData(Effect.WindowForceBlurRole, null);
    }

    // ------------------------------------------------------------ abrir
    animacaoEntrada(t) {
        if (this.reduzir && t !== "menu") {
            return { duracao: 120, curva: DESACELERA, extras: [] };
        }
        switch (t) {
        case "janela":
            return { duracao: 180, curva: DESACELERA, extras: [{ type: Effect.Scale, from: 0.96 }] };
        case "busca":
        case "painel":
            return { duracao: 160, curva: DESACELERA,
                     extras: [{ type: Effect.Translation, from: { value1: 0, value2: -8 }, to: { value1: 0, value2: 0 } }] };
        case "notificacao":
            return { duracao: 200, curva: DESACELERA,
                     extras: [{ type: Effect.Translation, from: { value1: 16, value2: 0 }, to: { value1: 0, value2: 0 } }] };
        case "menu":
            return { duracao: 80, curva: QEasingCurve.Linear, extras: [] };
        }
        return null;
    }

    janelaAdicionada(janela) {
        this.observarMinimizar(janela);
        if (effects.hasActiveFullScreenEffect || !janela.visible) {
            return;
        }
        if (effect.isGrabbed(janela, Effect.WindowAddedGrabRole)) {
            return;
        }
        const t = this.tipo(janela);
        const a = t && this.animacaoEntrada(t);
        if (!a) {
            return;
        }
        if (t !== "menu") {
            this.forcarPapeis(janela);
        }
        janela.animacaoAbrir = animate({
            window: janela,
            curve: a.curva,
            duration: animationTime(a.duracao),
            animations: a.extras.concat([{ type: Effect.Opacity, from: 0 }]),
        });
    }

    // ------------------------------------------------------------ fechar
    animacaoSaida(t) {
        if (this.reduzir && t !== "menu") {
            return { duracao: 100, curva: ACELERA, extras: [] };
        }
        switch (t) {
        case "janela":
            return { duracao: 140, curva: ACELERA, extras: [{ type: Effect.Scale, to: 0.96 }] };
        case "busca":
        case "painel":
        case "notificacao":
            return { duracao: 100, curva: ACELERA, extras: [] };
        case "menu":
            return { duracao: 80, curva: QEasingCurve.Linear, extras: [] };
        }
        return null;
    }

    janelaFechada(janela) {
        if (effects.hasActiveFullScreenEffect || !janela.visible || janela.skipsCloseAnimation) {
            return;
        }
        if (effect.isGrabbed(janela, Effect.WindowClosedGrabRole)) {
            return;
        }
        const t = this.tipo(janela);
        const a = t && this.animacaoSaida(t);
        if (!a) {
            return;
        }
        if (janela.animacaoAbrir) {
            cancel(janela.animacaoAbrir);
            delete janela.animacaoAbrir;
        }
        if (t !== "menu") {
            this.forcarPapeis(janela);
        }
        janela.animacaoFechar = animate({
            window: janela,
            curve: a.curva,
            duration: animationTime(a.duracao),
            animations: a.extras.concat([{ type: Effect.Opacity, to: 0 }]),
        });
    }

    dadosMudaram(janela, papel) {
        if (papel == Effect.WindowAddedGrabRole && janela.animacaoAbrir && effect.isGrabbed(janela, papel)) {
            cancel(janela.animacaoAbrir);
            delete janela.animacaoAbrir;
            this.limparPapeis(janela);
        } else if (papel == Effect.WindowClosedGrabRole && janela.animacaoFechar && effect.isGrabbed(janela, papel)) {
            cancel(janela.animacaoFechar);
            delete janela.animacaoFechar;
            this.limparPapeis(janela);
        }
    }

    // ------------------------------------------------------------ minimizar
    observarMinimizar(janela) {
        if (janela.draconicObservado) {
            return;
        }
        janela.draconicObservado = true;
        janela.minimizedChanged.connect(() => {
            if (janela.minimized) {
                this.minimizar(janela, true);
            } else {
                this.minimizar(janela, false);
            }
        });
    }

    minimizar(janela, indo) {
        if (effects.hasActiveFullScreenEffect) {
            return;
        }
        const atual = indo ? janela.animacaoMinimizar : janela.animacaoRestaurar;
        const oposta = indo ? janela.animacaoRestaurar : janela.animacaoMinimizar;
        if (oposta) {
            if (redirect(oposta, Effect.Backward)) {
                return;
            }
            cancel(oposta);
        }
        if (atual) {
            if (redirect(atual, Effect.Forward)) {
                return;
            }
            cancel(atual);
        }
        delete janela.animacaoMinimizar;
        delete janela.animacaoRestaurar;

        const icone = janela.iconGeometry;
        const semIcone = icone.width == 0 || icone.height == 0;
        let animacoes;
        let duracao;
        let curva;
        if (this.reduzir || semIcone) {
            // Some (ou aparece) no lugar.
            duracao = this.reduzir ? 100 : 160;
            curva = indo ? ACELERA : DESACELERA;
            animacoes = [{ type: Effect.Opacity, from: indo ? 1 : 0, to: indo ? 0 : 1 }];
        } else {
            const r = janela.geometry;
            const desloc = {
                value1: icone.x - r.x - (r.width - icone.width) / 2,
                value2: icone.y - r.y - (r.height - icone.height) / 2,
            };
            const zero = { value1: 0, value2: 0 };
            const cheio = { value1: r.width, value2: r.height };
            const pequeno = { value1: icone.width, value2: icone.height };
            duracao = 220;
            curva = SUAVE;
            animacoes = [
                { type: Effect.Size, from: indo ? cheio : pequeno, to: indo ? pequeno : cheio },
                { type: Effect.Translation, from: indo ? zero : desloc, to: indo ? desloc : zero },
                { type: Effect.Opacity, from: indo ? 1 : 0, to: indo ? 0 : 1 },
            ];
        }
        janela.setData(Effect.WindowForceBlurRole, true);
        const anim = animate({
            window: janela,
            curve: curva,
            duration: animationTime(duracao),
            keepAlive: false,
            animations: animacoes,
        });
        if (indo) {
            janela.animacaoMinimizar = anim;
        } else {
            janela.animacaoRestaurar = anim;
        }
    }
}

new MovimentoDraconic();
