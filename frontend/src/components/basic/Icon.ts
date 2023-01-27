
const ICONS_FOLDER = "/src/assets/icons/"
function svgIcon(filename: string): string {
    return ICONS_FOLDER + filename + ".svg"
}

/**
 * This enum contains all Icons that exist in the application.
 * It also stores the source of the icon for each enum entry.
 */
export enum Icon {
    INFO = svgIcon("info"),
    CLOSE = svgIcon("close"),
    HELP = svgIcon("help"),
    EDIT = svgIcon("edit"),
    DOWNLOAD = svgIcon("download"),
    UPLOAD_FILE = svgIcon("upload_file"),
    REFRESH = svgIcon("refresh"),
    EXPAND_DOWN = svgIcon("expand_down"),
    EXPAND_UP = svgIcon("expand_up"),
    EXPAND_RIGHT = svgIcon("expand_right"),
    EXPAND_LEFT = svgIcon("expand_left"),
    VISIBLE = svgIcon("visible"),
    VISIBLE_OFF = svgIcon("visible_off"),
    USER = svgIcon("user"),
}
