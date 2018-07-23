const alertEvent = (state = null, action) => {
    switch (action.type) {
    case 'ALERT':
        return action.status
    default:
        return state
    }
}

export default alertEvent