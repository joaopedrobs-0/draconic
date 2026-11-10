// Layout do Draconic (design/telas/Main.png, design/prototipo/Main.dc.html):
//   barra superior de 28 px, sólida: menu do sistema + menu global | idioma, bandeja, relógio
//   dock flutuante embaixo, centralizada, só ícones, com separador antes da Lixeira
//   papel de parede liso (pacote "Draconic", com versão clara e escura)
//
// O Plasma roda este script para usuários novos e quando alguém aplica o tema
// global com a opção de layout marcada.

// ---------------------------------------------------------------- barra superior
var barra = new Panel;
barra.location = "top";
barra.height = 28;
barra.floating = false;
barra.opacity = "opaque";      // usa solid/widgets/panel-background (surface.menubar)
barra.lengthMode = "fill";
barra.hiding = "none";

// Menu do sistema: o ícone é a marca do Draconic (start-here no tema de ícones).
var menu = barra.addWidget("org.kde.plasma.kickoff");
menu.currentConfigGroup = ["General"];
menu.writeConfig("icon", "start-here");

// Menu global do app em foco (Arquivo, Editar, Ver...).
barra.addWidget("org.kde.plasma.appmenu");

barra.addWidget("org.kde.plasma.panelspacer");

barra.addWidget("org.kde.plasma.keyboardlayout");
barra.addWidget("org.kde.plasma.systemtray");

// Relógio: "Seg 9 nov  21:20" (data ao lado da hora, 24 h).
var relogio = barra.addWidget("org.kde.plasma.digitalclock");
relogio.currentConfigGroup = ["Appearance"];
relogio.writeConfig("showDate", true);
relogio.writeConfig("dateDisplayFormat", "BesideTime");
relogio.writeConfig("dateFormat", "custom");
relogio.writeConfig("customDateFormat", "ddd d MMM");
relogio.writeConfig("use24hFormat", 2);

// ---------------------------------------------------------------- dock
var dock = new Panel;
dock.location = "bottom";
dock.height = 60;              // botões de 52 px + 4 px de margem em cima e embaixo
dock.floating = true;
dock.opacity = "translucent";  // vidro: translucent/widgets/panel-background
dock.lengthMode = "fit";
dock.alignment = "center";
dock.hiding = "none";

var tarefas = dock.addWidget("org.kde.plasma.icontasks");
tarefas.currentConfigGroup = ["General"];
tarefas.writeConfig("launchers", [
    "applications:org.kde.dolphin.desktop",
    "applications:org.mozilla.firefox.desktop",
    "applications:org.kde.konsole.desktop",
    "applications:org.kde.kwrite.desktop",
    "applications:org.kde.elisa.desktop",
    "applications:systemsettings.desktop"
].join(","));

dock.addWidget("org.kde.plasma.marginsseparator");
dock.addWidget("org.kde.plasma.trash");

// ---------------------------------------------------------------- papel de parede
var areas = desktopsForActivity(currentActivity());
for (var i = 0; i < areas.length; i++) {
    areas[i].wallpaperPlugin = "org.kde.image";
    areas[i].currentConfigGroup = ["Wallpaper", "org.kde.image", "General"];
    areas[i].writeConfig("Image", "file:///usr/share/wallpapers/Draconic/");
}
