import React, { Component } from 'react'
import { Grid } from '@material-ui/core'
import { withStyles } from '@material-ui/core/styles'
import Category from './Category'
import { FixedSpace } from 'components/Utils'
import APIClient from 'models/APIClient'

const styles = {}


class CategoryPage extends Component {
    state = {
        categories: null
    }

    componentDidMount() {
        APIClient.categories().then(response => {
            this.setState({ categories: response.data })
        }).catch(error => {
            console.log(error)
        })
    }

    render() {
        const { categories } = this.state
        if (!categories) return <div></div>
        return (
            <Grid container justify="center">
                <Grid item xs={11}><Category title="Main" categories={categories.slice(0, 2)}/></Grid>
                <Grid item xs={12}><FixedSpace size="xl2"/></Grid>
                <Grid item xs={11}><Category title="Specific Projects" categories={categories.slice(2)}/></Grid>
            </Grid>
        )
    }
}

export default withStyles(styles)(CategoryPage)