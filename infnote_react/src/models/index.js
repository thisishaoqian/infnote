import { createStore } from 'redux'
import reducers from './reducers'

export { default as User } from './User'
export { default as SignUser } from './SignUser'
export { default as Post } from './Post'
export { default as APIClient } from './APIClient'

export const Store = createStore(reducers)