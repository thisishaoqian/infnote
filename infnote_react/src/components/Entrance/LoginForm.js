import React, { Component } from 'react'
import { Redirect, withRouter } from 'react-router-dom'
import { withStyles } from '@material-ui/core/styles'
import { Card, CardActions, CardContent, Typography, Button, Grid, TextField, Checkbox, FormControlLabel, colors } from '@material-ui/core'
import { FixedSpace, Line } from 'components/Utils'


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
    hidden: {
        display: 'none',
    },
    errorHint: {
        color: 'red',
    }
}

class LoginForm extends Component {

    constructor() {
        super()
        this.state = {
            email: '',
            password: '',
            isAuthed: User.current().user_id ? true : false,
            error: null,
        }
    }

    handleChangeEmail = event => this.setState({ email: event.target.value, error: null })
    handleChangePassword = event => this.setState({ password: event.target.value, error: null })

    handleLogin = () => {
        User.login(this.state.email, this.state.password).then(user => {
            if (user) {
                this.setState({ isAuthed: true })
            }
        }).catch(error => {
            this.setState({ error })
        })
    }

    render() {
        const { classes } = this.props
        const { from } = this.props.location.state || { from: HOME }
        if ( this.state.isAuthed ) {
            return (<Redirect to={from}/>)
        }

        return (
            <Grid item xs={11} sm={8} md={5} lg={4} xl={3}>
                <Card className="paper">
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
                        <Typography className={ this.state.error ? classes.errorHint : classes.hidden }>Wrong email address or password</Typography>
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
                            Don't have an account? <Button size="small" style={{fontWeight: 'bold'}} onClick={() => this.props.history.push('/sign/up/')}>Sign Up</Button>
                        </Typography>
                    </CardActions>
                    <FixedSpace size="sm" />
                </Card>
            </Grid>
        )
    }
}

export default withRouter(withStyles(styles)(LoginForm))
