import User from '../User'

const userEvent = (state = User.current(), action) => {
    switch (action.type) {
    case 'USER_CHANGED':
        return action.user
    default:
        return state
    }
}

export default userEvent