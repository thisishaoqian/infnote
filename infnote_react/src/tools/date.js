import { sprintf } from 'sprintf-js'

function format(seconds) {
    let date = new Date(null)
    date.setSeconds(seconds)

    let now = new Date()

    let delta = (now - date) / 1000
    
    let result = 'Wrong Date Format'

    if (delta < 60) {
        result = 'Just now'
    } else if (delta < 60 * 60) {
        result = Math.floor(delta / 60) + 'm ago'
    } else if (delta < 60 * 60 * 3) {
        result = Math.floor(delta/ 60 / 60) + 'h ago'
    } else if (now.getDate() === date.getDate() && delta < 60 * 60 * 24) {
        result = sprintf('%02d:%02d', date.getHours(), date.getMinutes())
    } else if (now.getDate() - date.getDate() < 2 && delta < 60 * 60 * 24 * 2) {
        result = sprintf('Yesterday, %02d:%02d', date.getHours(), date.getMinutes())
    } else if (now.getFullYear() === date.getFullYear()) {
        result = sprintf(
            '%02d/%02d, %02d:%02d',
            date.getMonth() + 1, 
            date.getDate(),
            date.getHours(), 
            date.getMinutes()
        )
    } else {
        result = sprintf(
            '%d/%02d/%02d, %02d:%02d',
            date.getFullYear(), 
            date.getMonth() + 1, 
            date.getDate(),
            date.getHours(), 
            date.getMinutes()
        )
    }

    return result
}

export default format