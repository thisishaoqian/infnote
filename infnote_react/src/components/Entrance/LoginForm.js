import React, { Component } from 'react'
import { Redirect, withRouter } from 'react-router-dom'
import { withStyles } from '@material-ui/core/styles'
import { Card, CardActions, CardContent, Typography, Button, Grid, TextField, Checkbox, FormControlLabel, colors } from '@material-ui/core'
import { FixedSpace, Line } from 'components/Utils'
import background from './background.png'

import { User } from 'models'
import { HOME } from 'config'


const styles = {
    subtitle: {
        fontSize: 15,
        fontFamily: 'Arial Black'
    },
    title: {
        fontSize: 35,
        fontFamily: 'Arial Black'
    },
    inputCard: {
        borderStyle: 'solid',
        borderWidth: 1,
        borderColor: '#EEE',
        borderRadius: 3,
        boxShadow: '1px 1px 3px #EEE',
    },
    innerShadow: {
        boxShadow: '1px 1px 3px #EEE inset',
    },
    background: {
        backgroundImage: 'url(' + background + ')',
        backgroundPosition: '50% 50%',
        backgroundSize: 'cover',
        backgroundRepeat: 'no-repeat',
        position: 'fixed',
        top: 0, left: 0, right: 0, bottom: 0,
        zIndex: -1,
    }
}

class LoginForm extends Component {

    constructor() {
        super()
        this.state = {
            email: '',
            password: '',
            isAuthed: false,
        }
    }

    handleChangeEmail = event => this.setState({ email: event.target.value })
    handleChangePassword = event => this.setState({ password: event.target.value })

    handleLogin = () => {
        User.login(this.state.email, this.state.password).then(user => {
            if (user) {
                this.setState({ isAuthed: true })
            }
        })
    }

    render() {
        const { from } = this.props.location.state || { from: { pathname: HOME } }
        const { classes } = this.props
        const { isAuthed } = this.state

        if (isAuthed) {
            return (
                <Redirect to={from}/>
            )
        }

        return (
            <Grid container className="full-width full-height" justify="center" alignItems="center">
                <div className={classes.background}></div>
                <Grid item xs={11} sm={8} md={5} lg={4} xl={2}>
                    <Card>
                        <FixedSpace size="sm"/>
                        <CardContent style={{
                            paddingLeft: '10%',
                            paddingRight: '10%',
                        }}>
                            <Typography className={classes.subtitle} variant="subheading" align="center" color="primary">
                                Welcome to
                            </Typography>
                            <Typography className={classes.title} align="center" color="primary">
                                INFNOTE
                            </Typography>
                            <Typography className={classes.subtitle} variant="subheading" align="center" style={{color: colors.grey.A200}}>
                                A Blockchain Based Forum
                            </Typography>
                            <FixedSpace size="sm"/>
                            <div className={classes.inputCard}>
                                <div className={classes.innerShadow}>
                                    <Grid container justify="center">
                                        <Grid item xs={10}>
                                            <FixedSpace size="xs3" />
                                            <TextField 
                                                id="email" 
                                                type="email" 
                                                label="Email Address" 
                                                InputProps={{disableUnderline: true}}
                                                fullWidth
                                                onChange={this.handleChangeEmail}
                                                value={this.state.email}
                                            />
                                            <FixedSpace size="xs2" />
                                        </Grid>
                                        <Grid item xs={12}><Line gutter={5} /></Grid>
                                        <Grid item xs={10}>
                                            <FixedSpace size="xs3" />
                                            <TextField 
                                                id="password" 
                                                type="password" 
                                                label="Password" 
                                                InputProps={{disableUnderline: true}} 
                                                fullWidth
                                                onChange={this.handleChangePassword}
                                                value={this.state.password}
                                            />
                                            <FixedSpace size="xs2" />
                                        </Grid>
                                    </Grid>
                                </div>
                            </div>
                            <FixedSpace size="xs"/>
                            <Grid container>
                                <Grid item xs={6}>
                                    <FormControlLabel 
                                        control={
                                            <Checkbox color="primary" />
                                        } 
                                        label="Remember me"
                                    />
                                </Grid>
                                <Grid item xs={6} className={classes.forget}>
                                    <Grid container className="full-height" justify="flex-end" alignItems="center"><Grid item><Button size="small">Forget Password</Button></Grid></Grid>
                                </Grid>
                            </Grid>
                            <FixedSpace size="md"/>
                            <Button variant="raised" color="primary" size="large" style={{fontWeight: 'bold'}} fullWidth onClick={this.handleLogin}>Login</Button>
                        </CardContent>
                        <CardActions>
                            <Typography className="full-width" align="center">
                                Don't have an account? <Button size="small" style={{fontWeight: 'bold'}}>Sign Up</Button>
                            </Typography>
                        </CardActions>
                        <FixedSpace size="sm" />
                    </Card>
                </Grid>
            </Grid>
        )
    }
}

export default withRouter(withStyles(styles)(LoginForm))
