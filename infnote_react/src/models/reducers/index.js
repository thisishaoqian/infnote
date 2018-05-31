import { combineReducers } from 'redux'
import userEvent from './userEvent'
import postEvent from './postEvent'

export default combineReducers({userEvent, postEvent})