import React, { Component } from 'react'
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom'
import { createMuiTheme, MuiThemeProvider } from '@material-ui/core/styles'
import { CssBaseline } from '@material-ui/core'
import JssProvider from 'react-jss/lib/JssProvider'
import { create } from 'jss'
import { createGenerateClassName, jssPreset } from '@material-ui/core/styles'

import { Entrance } from '../Entrance'
import App from './App'
import { User } from 'models'


const theme = createMuiTheme({
    palette: {
        primary: {
            main: '#262D47',
        },
        secondary: {
            main: '#9FE0FC',
        },
        textPrimary: {
            main: '#4A4A4A',
        },
        paperBackground: {
            main: 'white',
        }
    },
    typography: {
        fontFamily: [
            '"Avenir Next"', 
            'Roboto',
            '"Helvetica Neue"',
            'Arial',
            'sans-serif',
        ].join(',')
    }
})
const generateClassName = createGenerateClassName()
const jss = create(jssPreset())
// We define a custom insertion point that JSS will look for injecting the styles in the DOM.
jss.options.insertionPoint = 'jss-insertion-point'


class BaseApp extends Component {
    componentWillMount() {
        User.recover()
    }
    render() {
        return (
            <MuiThemeProvider theme={theme}>
                <CssBaseline />
                <JssProvider jss={jss} generateClassName={generateClassName}>
                    <Router>
                        <Switch>
                            <Route path="/sign" component={Entrance}/>
                            <App />
                        </Switch>
                    </Router>
                </JssProvider>
            </MuiThemeProvider>
        )
    }
}

export default BaseApp
