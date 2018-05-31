import React, { Component } from 'react'
import { withStyles } from '@material-ui/core/styles'
import { Grid } from '@material-ui/core'
import { Topic, PostForm, Breadcrumb } from './components'
import { FixedSpace } from 'components/Utils'

import { Post } from 'models'

const styles = {

}

class TopicPage extends Component {
    state = {
        post: null,
    }

    componentWillMount() {
        Post.retreive(this.props.match.params.id).then(post => {
            this.setState({ post })
        })
    }

    render () {
        const { post } = this.state
        if (!post) return (<div></div>)
        return (
            <Grid container>
                <Grid container justify="center">
                    <Grid item xs={11}><Breadcrumb crumb={['General Discussion', 'Title']} /></Grid>
                </Grid>
                <Grid container justify="center">
                    <Grid item xs={11}><Topic post={this.state.post}/></Grid>
                </Grid>
                <Grid container><FixedSpace size="md"/></Grid>
                <Grid container justify="center">
                    <Grid item xs={11}><PostForm type="Reply" post={this.state.post}/></Grid>
                </Grid>
                <Grid container><FixedSpace size="md"/></Grid>
            </Grid>
        )
    }
}

export default withStyles(styles)(TopicPage)