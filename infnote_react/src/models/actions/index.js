export const changeUser = user => ({
    type: 'USER_CHANGED',
    user
})

export const sendPost = post => ({
    type: 'SEND_POST',
    post
})

export const alertAction = status => ({
    type: 'ALERT',
    status
})