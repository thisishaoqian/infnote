import React, { Component } from 'react'
import { withStyles } from '@material-ui/core/styles'
import { Grid } from '@material-ui/core'
import { TopicList, PostForm, Breadcrumb } from './components'
import { FixedSpace } from 'components/Utils'

const styles = {

}

class TopicListPage extends Component {
    render () {
        return (
            <Grid container>    
                <Grid container justify="center">
                    <Grid item xs={11}><Breadcrumb crumb={['General Discussion']} /></Grid>
                </Grid>
                <Grid container justify="center">
                    <Grid item xs={11}><TopicList /></Grid>
                </Grid>
                <Grid container><FixedSpace size="md"/></Grid>
                <Grid container justify="center">
                    <Grid item xs={11}><PostForm type="Topic"/></Grid>
                </Grid>
                <Grid container><FixedSpace size="md"/></Grid>
            </Grid>
        )
    }
}

export default withStyles(styles)(TopicListPage)