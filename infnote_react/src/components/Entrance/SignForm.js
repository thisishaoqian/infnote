import React, { Component } from 'react'
import { Redirect, withRouter } from 'react-router-dom'
import { withStyles } from '@material-ui/core/styles'
import { Card, CardContent, Typography, Button, Grid, Tabs, Tab, TextField, Select, MenuItem } from '@material-ui/core'
import SwipeableViews from 'react-swipeable-views'
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
    }
    
    handleChange = (event, value) => {
        this.setState({ index: value })
    }

    render() {
        const { classes } = this.props
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
                            onChange={this.handleChange}
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
                                <Grid item xs={11}>
                                    <Typography className={classes.label} gutterBottom>Username</Typography>
                                    <TextField 
                                        id="username" 
                                        type="text"  
                                        InputProps={{disableUnderline: true}}
                                        className={classes.textField}
                                        fullWidth
                                    />
                                    <FixedSpace size="sm"/>
                                    <Typography className={classes.label} gutterBottom>Nickname</Typography>
                                    <TextField 
                                        id="nickname" 
                                        type="text"  
                                        InputProps={{disableUnderline: true}}
                                        className={classes.textField}
                                        fullWidth
                                    />
                                    <FixedSpace size="sm"/>
                                    <Typography className={classes.label} gutterBottom>Email Address</Typography>
                                    <TextField 
                                        id="email" 
                                        type="email"  
                                        InputProps={{disableUnderline: true}}
                                        className={classes.textField}
                                        fullWidth
                                    />
                                    <FixedSpace size="xs2"/>
                                    <Grid container justify="space-between" alignItems="center">
                                        <Grid item xs={6}>
                                            <TextField 
                                                id="code" 
                                                type="text"
                                                placeholder="Input Verification Code"
                                                InputProps={{disableUnderline: true}}
                                                className={classes.textField}
                                                fullWidth
                                            />
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
                                        fullWidth
                                    />
                                    <FixedSpace size="md"/>
                                    <Button variant="raised" color="primary" size="large" style={{fontWeight: 'bold'}} fullWidth>Next</Button>
                                </Grid>
                            </Grid>
                            <Grid container justify="center">
                                <Grid item xs={11}>
                                    <Grid container justify="space-between" alignItems="center">
                                        <Grid item xs={5}>
                                            <Typography className={classes.label} gutterBottom>Gender</Typography>
                                            <Select 
                                                id="gender" 
                                                value={0}
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
                                                defaultValue="1991-01-01"
                                                className={classes.textField}
                                                InputLabelProps={{
                                                    shrink: true,
                                                }}
                                                InputProps={{disableUnderline: true}}
                                                fullWidth
                                            />
                                        </Grid>
                                    </Grid>
                                    <FixedSpace size="sm"/>
                                    <Typography className={classes.label} gutterBottom>Location</Typography>
                                    <TextField 
                                        id="location" 
                                        type="text"  
                                        InputProps={{disableUnderline: true}}
                                        className={classes.textField}
                                        fullWidth
                                    />
                                    <FixedSpace size="sm"/>
                                    <Typography className={classes.label} gutterBottom>Website</Typography>
                                    <TextField 
                                        id="website" 
                                        type="text"  
                                        className={classes.textField}
                                        InputProps={{disableUnderline: true}} 
                                        fullWidth
                                    />
                                    <FixedSpace size="sm"/>
                                    <Typography className={classes.label} gutterBottom>Bio</Typography>
                                    <TextField 
                                        id="bio" 
                                        type="text"
                                        rows="5"
                                        className={classes.textField}
                                        InputProps={{disableUnderline: true}} 
                                        fullWidth
                                        multiline
                                    />
                                    <FixedSpace size="md"/>
                                    <Button variant="raised" color="primary" size="large" style={{fontWeight: 'bold'}} fullWidth>Next</Button>
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
