import React, { Component } from 'react'
import { Redirect, withRouter } from 'react-router-dom'
import { withStyles } from '@material-ui/core/styles'
import { Card, CardContent, Typography, Button, Grid, Tabs, Tab, TextField, Select, MenuItem } from '@material-ui/core'
import SwipeableViews from 'react-swipeable-views'
import { FixedSpace, Line, showAlert } from 'components/Utils'

import { User, SignUser } from 'models'
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
    hint: {
        color: '#888',
    },
    errorHint: {
        color: 'red',
    },
    textField: {
        borderWidth: 1,
        borderColor: '#CCC',
        borderRadius: 5,
        borderStyle: 'solid',
        padding: '5px 15px'
    },
    label: {
        fontWeight: 500,
    }
}

class SignForm extends Component {
    state = {
        email: '',
        password: '',
        isAuthed: User.current().user_id ? true : false,
        error: null,
        index: 0,
        gender: 0,
        birthday: '1991-01-01',
    }
    
    handleIndexChange = (event, value) => {
        this.setState({ index: value })
    }

    handleFieldChange = (event) => {
        let field = event.target.id
        let value = event.target.value
        if (!field) {
            field = event.target.name
        }
        if (field === 'birthday') {
            field = 'date_birthday'
            let date = new Date(value)
            value = date.getTime() / 1000
        }
        this.setState({[field]: value})
    }

    handleSignUp = () => {
        let sign = new SignUser(this.state)
        sign.signUp().then(() => {
            User.login(sign.email, sign.password).then(() => {
                User.current().submit().then(() => {
                    this.props.history.goBack()
                }).catch(error => showAlert('Error', error.response.data.message))
            }).catch(error => showAlert('Error', error.response.data.message))
        }).catch(error => {
            if (error.response.status < 500) {
                this.setState({ error: error.response.data })
            } else {
                showAlert()
            }
        })
    }

    render() {
        const { classes } = this.props
        const { error } = this.state
        const { from } = this.props.location.state || { from: HOME }
        if ( this.state.isAuthed ) {
            return (<Redirect to={from}/>)
        }

        return (
            <Grid item xs={11}>
                <Card className="paper">
                    <FixedSpace size="sm"/>
                    <CardContent style={{
                        paddingLeft: '10%',
                        paddingRight: '10%',
                    }}>
                        <Typography className={classes.subtitle} variant="subheading" align="center" color="primary">
                            SIGN UP TO
                        </Typography>
                        <Typography className={classes.title} align="center" color="primary">
                            INFNOTE
                        </Typography>
                        <FixedSpace size="md"/>
                        <Tabs
                            value={this.state.index}
                            onChange={this.handleIndexChange}
                            indicatorColor="primary"
                            textColor="primary"
                            centered
                        >
                            <Tab label="1.Basic Information" />
                            <Tab label="2.Other Information" />
                            <Tab label="3.Social Profiles" />
                        </Tabs>
                        <Line />
                        <FixedSpace size="sm"/>
                        <SwipeableViews index={this.state.index}>
                            <Grid container justify="center">
                                <Grid item xs={12} sm={11} md={8} lg={6}>
                                    <Typography className={classes.label} gutterBottom>Username</Typography>
                                    <TextField 
                                        id="username" 
                                        type="text"  
                                        InputProps={{disableUnderline: true}}
                                        className={classes.textField}
                                        onChange={this.handleFieldChange}
                                        fullWidth
                                    />
                                    <Typography className={ error && error.username ? classes.errorHint : classes.hidden }>{ error && error.username ? error.username : '' }</Typography>
                                    <FixedSpace size="sm"/>
                                    <Typography className={classes.label} gutterBottom>Nickname</Typography>
                                    <TextField 
                                        id="nickname" 
                                        type="text"  
                                        InputProps={{disableUnderline: true}}
                                        className={classes.textField}
                                        onChange={this.handleFieldChange}
                                        fullWidth
                                    />
                                    <Typography className={ error && error.nickname ? classes.errorHint : classes.hidden }>{ error && error.nickname ? error.nickname : '' }</Typography>
                                    <FixedSpace size="sm"/>
                                    <Typography className={classes.label} gutterBottom>Email Address</Typography>
                                    <TextField 
                                        id="email" 
                                        type="email"  
                                        InputProps={{disableUnderline: true}}
                                        className={classes.textField}
                                        onChange={this.handleFieldChange}
                                        fullWidth
                                    />
                                    <Typography className={ error && error.email ? classes.errorHint : classes.hidden }>{ error && error.email ? error.email : '' }</Typography>
                                    <FixedSpace size="xs2"/>
                                    <Grid container justify="space-between" alignItems="center">
                                        <Grid item xs={6}>
                                            <TextField 
                                                id="code" 
                                                type="text"
                                                placeholder="Input Verification Code"
                                                InputProps={{disableUnderline: true}}
                                                className={classes.textField}
                                                onChange={this.handleFieldChange}
                                                fullWidth
                                            />
                                            <Typography className={ error && error.code ? classes.errorHint : classes.hidden }>{ error && error.code ? error.code : '' }</Typography>
                                        </Grid>
                                        <Grid item xs={5}><Button variant="raised" color="primary" fullWidth>Send Verification</Button></Grid>
                                    </Grid>
                                    <FixedSpace size="xs3"/>
                                    <Typography className={classes.hint}>We will send you bitcoins by email to help you start :) </Typography>
                                    <FixedSpace size="sm"/>
                                    <Typography className={classes.label} gutterBottom>Password</Typography>
                                    <TextField 
                                        id="password" 
                                        type="password"  
                                        className={classes.textField}
                                        InputProps={{disableUnderline: true}} 
                                        onChange={this.handleFieldChange}
                                        fullWidth
                                    />
                                    <Typography className={ error && error.password ? classes.errorHint : classes.hidden }>{ error && error.password ? error.password : '' }</Typography>
                                    <FixedSpace size="md"/>
                                    <Button variant="raised" color="primary" size="large" style={{fontWeight: 'bold'}} fullWidth onClick={() => this.handleIndexChange(null, 1)}>Next</Button>
                                </Grid>
                            </Grid>
                            <Grid container justify="center">
                                <Grid item xs={12} sm={11} md={8} lg={6}>
                                    <Grid container justify="space-between" alignItems="center">
                                        <Grid item xs={5}>
                                            <Typography className={classes.label} gutterBottom>Gender</Typography>
                                            <Select 
                                                id="gender" 
                                                value={this.state.gender}
                                                onChange={this.handleFieldChange}
                                                inputProps={
                                                    {id: 'gender', name: 'gender'}
                                                }
                                                fullWidth
                                            >
                                                <MenuItem value={0}>
                                                    <em>Other</em>
                                                </MenuItem>
                                                <MenuItem value={1}>Male</MenuItem>
                                                <MenuItem value={2}>Female</MenuItem>
                                            </Select>
                                        </Grid>
                                        <Grid item xs={6}>
                                            <Typography className={classes.label} gutterBottom>Birthday</Typography>
                                            <TextField
                                                id="birthday"
                                                type="date"
                                                defaultValue={this.state.birthday}
                                                className={classes.textField}
                                                InputLabelProps={{
                                                    shrink: true,
                                                }}
                                                InputProps={{disableUnderline: true}}
                                                onChange={this.handleFieldChange}
                                                fullWidth
                                            />
                                            <Typography className={ error && error.date_birthday ? classes.errorHint : classes.hidden }>{ error && error.date_birthday ? error.date_birthday : '' }</Typography>
                                        </Grid>
                                    </Grid>
                                    <FixedSpace size="sm"/>
                                    <Typography className={classes.label} gutterBottom>Location</Typography>
                                    <TextField 
                                        id="location" 
                                        type="text"  
                                        InputProps={{disableUnderline: true}}
                                        className={classes.textField}
                                        onChange={this.handleFieldChange}
                                        fullWidth
                                    />
                                    <Typography className={ error && error.location ? classes.errorHint : classes.hidden }>{ error && error.location ? error.location : '' }</Typography>
                                    <FixedSpace size="sm"/>
                                    <Typography className={classes.label} gutterBottom>Website</Typography>
                                    <TextField 
                                        id="website" 
                                        type="text"  
                                        className={classes.textField}
                                        InputProps={{disableUnderline: true}} 
                                        onChange={this.handleFieldChange}
                                        fullWidth
                                    />
                                    <Typography className={ error && error.website ? classes.errorHint : classes.hidden }>{ error && error.website ? error.website : '' }</Typography>
                                    <FixedSpace size="sm"/>
                                    <Typography className={classes.label} gutterBottom>Bio</Typography>
                                    <TextField 
                                        id="bio" 
                                        type="text"
                                        rows="5"
                                        className={classes.textField}
                                        InputProps={{disableUnderline: true}} 
                                        onChange={this.handleFieldChange}
                                        fullWidth
                                        multiline
                                    />
                                    <Typography className={ error && error.bio ? classes.errorHint : classes.hidden }>{ error && error.bio ? error.bio : '' }</Typography>
                                    <FixedSpace size="md"/>
                                    <Button variant="raised" color="primary" size="large" style={{fontWeight: 'bold'}} fullWidth onClick={() => this.handleIndexChange(null, 2)}>Next</Button>
                                </Grid>
                            </Grid>
                            <Grid container justify="center">
                                <Grid item xs={12} sm={11} md={8} lg={6}>
                                    <Typography className={classes.label} gutterBottom>QQ</Typography>
                                    <TextField 
                                        id="qq" 
                                        type="text"  
                                        InputProps={{disableUnderline: true}}
                                        className={classes.textField}
                                        onChange={this.handleFieldChange}
                                        fullWidth
                                    />
                                    <Typography className={ error && error.qq ? classes.errorHint : classes.hidden }>{ error && error.qq ? error.qq : '' }</Typography>
                                    <FixedSpace size="sm"/>
                                    <Typography className={classes.label} gutterBottom>Wechat</Typography>
                                    <TextField 
                                        id="wechat" 
                                        type="text"  
                                        InputProps={{disableUnderline: true}}
                                        className={classes.textField}
                                        onChange={this.handleFieldChange}
                                        fullWidth
                                    />
                                    <Typography className={ error && error.wechat ? classes.errorHint : classes.hidden }>{ error && error.wechat ? error.wechat : '' }</Typography>
                                    <FixedSpace size="sm"/>
                                    <Typography className={classes.label} gutterBottom>Weibo</Typography>
                                    <TextField 
                                        id="weibo" 
                                        type="text"  
                                        InputProps={{disableUnderline: true}}
                                        className={classes.textField}
                                        onChange={this.handleFieldChange}
                                        fullWidth
                                    />
                                    <Typography className={ error && error.weibo ? classes.errorHint : classes.hidden }>{ error && error.weibo ? error.weibo : '' }</Typography>
                                    <FixedSpace size="sm"/>
                                    <Typography className={classes.label} gutterBottom>Facebook</Typography>
                                    <TextField 
                                        id="facebook" 
                                        type="text"  
                                        InputProps={{disableUnderline: true}}
                                        className={classes.textField}
                                        onChange={this.handleFieldChange}
                                        fullWidth
                                    />
                                    <Typography className={ error && error.facebook ? classes.errorHint : classes.hidden }>{ error && error.facebook ? error.facebook : '' }</Typography>
                                    <FixedSpace size="sm"/>
                                    <Typography className={classes.label} gutterBottom>Twitter</Typography>
                                    <TextField 
                                        id="twitter" 
                                        type="text"  
                                        InputProps={{disableUnderline: true}}
                                        className={classes.textField}
                                        onChange={this.handleFieldChange}
                                        fullWidth
                                    />
                                    <Typography className={ error && error.twitter ? classes.errorHint : classes.hidden }>{ error && error.twitter ? error.twitter : '' }</Typography>
                                    <FixedSpace size="md"/>
                                    <Button variant="raised" color="primary" size="large" style={{fontWeight: 'bold'}} fullWidth onClick={this.handleSignUp}>Sign Up</Button>
                                </Grid>
                            </Grid>
                        </SwipeableViews>
                    </CardContent>
                    <FixedSpace size="md"/>
                </Card>
            </Grid>
        )
    }
}

export default withRouter(withStyles(styles)(SignForm))
