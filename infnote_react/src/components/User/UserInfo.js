import React, { Component } from 'react'
import { Grid, Card, CardContent, Typography, Button } from '@material-ui/core'
import { FixedSpace, Line } from '../Utils'
import { withStyles } from '@material-ui/core/styles'
import background from 'assets/background.png'
import classNames from 'classnames'

import { User, Store } from 'models'
import { facebook, qq, twitter, website, wechat, weibo } from './icons'
import avatar from 'assets/avatar-placeholder.svg'

const styles = theme => {
    return {
        background: {
            backgroundImage: 'url(' + background + ')',
            backgroundPosition: '50% 50%',
            backgroundSize: 'cover',
            backgroundRepeat: 'no-repeat',
            position: 'fixed',
            top: 0, left: 0, right: 0, bottom: 0,
            zIndex: -1,
        },
        avatar: {
            // background: '#ccc',
            width: 80,
            height: 80,
            borderRadius: 5,
            textAlign: 'center',
        },
        title: {
            fontSize: 20,
            fontWeight: 'bold'
        },
        table: {
            fontFamily: theme.typography.fontFamily,
            fontSize: 14,
            fontWeight: 500,
        },
        cols: {
            '&>div': {
                height: 30,
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center',
            },
            '&>div:nth-child(2n+1)': {
                color: '#9B9B9B'
            }
        }
    }
}


class UserInfo extends Component {

    state = {
        user: User.placeholder()
    }

    componentWillMount() {
        this.setState({ user: User.current() })
        this.unsubscribe = Store.subscribe(() => {
            const user = Store.getState().userEvent
            this.setState({ user })
        })
    }

    componentWillUnmount() {
        this.unsubscribe()
    }

    render() {
        const { classes } = this.props
        const { user } = this.state
        return (
            <Grid container className="full-width" justify="center" alignItems="center">
                <div className={classes.background}></div>
                <Grid item xs={11} sm={8} md={5} lg={4} xl={3}>
                    <Card className="paper">
                        <FixedSpace size="sm"/>
                        <CardContent style={{
                            paddingLeft: '10%',
                            paddingRight: '10%',
                        }}>
                            <Grid container justify="center">
                                <div className={classes.avatar}><img src={avatar} alt="Avatar" width="80" height="80"/></div>
                            </Grid>
                            <FixedSpace size="xs" />
                            <Typography className={classes.title} align="center" color="primary">{user.nickname}</Typography>
                            <FixedSpace size="md" />
                            <Line width={3}></Line>
                            <FixedSpace size="xs" />
                            <Grid container className={classNames(classes.table, classes.cols)}>
                                <Grid item xs={4}>Email</Grid><Grid item xs={8}>{user.email}</Grid>
                                <Grid item xs={4}>Public Address</Grid><Grid item xs={8}>{user.public_address}</Grid>
                                <Grid item xs={4}>Gender</Grid><Grid item xs={8}>{user.getGender()}</Grid>
                                <Grid item xs={4}>Location</Grid><Grid item xs={8}>{user.location}</Grid>
                                <Grid item xs={4}>Bio</Grid><Grid item xs={8}>{user.bio}</Grid>
                            </Grid>
                            <FixedSpace size="xs" />
                            <Line width={3}></Line>
                            <FixedSpace size="xs" />
                            <Grid container className={classes.table}>
                                <Grid item xs={12}>
                                    <img src={website} alt="website"></img>
                                    <Typography>{user.website}</Typography>
                                </Grid>
                                <Grid item xs={12}><FixedSpace size="xs2" /></Grid>
                                <Grid item xs={4}>
                                    <img src={qq} alt="qq"></img>
                                    <Typography>{user.qq}</Typography>
                                </Grid>
                                <Grid item xs={4}>
                                    <img src={wechat} alt="wechat"></img>
                                    <Typography>{user.wechat}</Typography>
                                </Grid>
                                <Grid item xs={4}>
                                    <img src={weibo} alt="weibo"></img>
                                    <Typography>{user.weibo}</Typography>
                                </Grid>
                                <Grid item xs={12}><FixedSpace size="xs2" /></Grid>
                                <Grid item xs={4}>
                                    <img src={facebook} alt="facebook"></img>
                                    <Typography>{user.facebook}</Typography>
                                </Grid>
                                <Grid item xs={4}>
                                    <img src={twitter} alt="twitter"></img>
                                    <Typography>{user.twitter}</Typography>
                                </Grid>
                            </Grid>
                            <FixedSpace size="md" />
                            <Button variant="raised" color="primary" size="large" style={{fontWeight: 'bold'}} fullWidth>Save</Button>
                        </CardContent>
                        <FixedSpace size="sm" />
                    </Card>
                </Grid>
                <Grid item xs={12}><FixedSpace size="lg"/></Grid>
            </Grid>
        )
    }
}

export default withStyles(styles)(UserInfo)