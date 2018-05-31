const postEvent = (state = null, action) => {
    switch (action.type) {
    case 'SEND_POST':
        return action.post
    default:
        return state
    }
}

export default postEvent