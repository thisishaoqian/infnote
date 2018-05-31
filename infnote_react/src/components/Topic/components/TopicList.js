import React, { Component } from 'react'
import { withRouter } from 'react-router'
import { withStyles } from '@material-ui/core/styles'
import { Redirect } from 'react-router-dom'
import classNames from 'classnames'
import { Paper, Typography, Table, TableBody, TableCell, TableHead, TableFooter, TablePagination, TableRow } from '@material-ui/core'
import { FixedSpace } from 'components/Utils'

import { Post, Store } from 'models'

const styles = theme => {
    const colors = theme.palette
    return {
        titleColumn: {
            width: '60%',
        },
        tableTitle: {
            fontSize: '1.6em',
            fontWeight: 'bold',
            paddingTop: 15,
            paddingLeft: 25,
            paddingBottom: 15,
            color: colors.textPrimary.main,
        },
        leftSpacing: {
            paddingLeft: 60
        },
        tableHeadRow: {
            background: colors.grey[200],
            '&>*': {
                fontSize: '1.1em',
                fontWeight: 600,
                color: colors.textPrimary.main,
            }
        },
        tableBodyRow: {
            '&>*': {
                fontWeight: 600,
                color: colors.textPrimary.main,
            }
        }
    }
}

class TopicList extends Component {
    constructor(props) {
        super()
        this.props = props
        this.state = {
            rowsPerPage: 20,
            page: 0,
            count: 0,
            selected: null,
            posts: []
        }

        this.reloadData()
    }

    reloadData = () => {
        Post.retreiveList().then(data => {
            this.setState({posts: data.posts, count: data.count})
        }).catch(error => {
            console.log(error)
        })
    }

    componentWillMount() {
        this.unsubscribe = Store.subscribe(() => {
            this.reloadData()
        })
    }

    componentWillUnmount() {
        this.unsubscribe()
    }

    handleRowClick = item => {
        this.setState({ selected: item })
    }

    handleChangePage = (event, page) => {
        this.setState({ page })
    }

    handleChangeRowsPerPage = event => {
        this.setState({ rowsPerPage: event.target.value })
    }

    render() {
        const { classes } = this.props
        const { rowsPerPage, page, posts, selected } = this.state
        if (selected) {
            return (<Redirect push to={'/topic/' + selected.post_id}/>)
        }
        return (
            <Paper className="paper">
                <FixedSpace size="xs3" className="paper-decorator"/>
                <Typography className={classes.tableTitle}>General Discussion</Typography>
                <Table>
                    <TableHead>
                        <TableRow className={classes.tableHeadRow}>
                            <TableCell className={classes.leftSpacing}>Topic</TableCell>
                            <TableCell>Started by</TableCell>
                            <TableCell>Replies</TableCell>
                            <TableCell>Last post</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {posts.map((item, index) => {
                            return (
                                <TableRow hover key={index} className={classes.tableBodyRow} onClick={() => this.handleRowClick(item)}>
                                    <TableCell className={classNames(classes.titleColumn, classes.leftSpacing)}>
                                        {item.title}
                                    </TableCell>
                                    <TableCell>{item.public_key}</TableCell>
                                    <TableCell>{item.replies}</TableCell>
                                    <TableCell>Today 03:32:54 am<br />by {item.last}</TableCell>
                                </TableRow>
                            )
                        })}
                    </TableBody>
                    <TableFooter>
                        <TableRow>
                            <TablePagination 
                                count={this.state.count}
                                rowsPerPage={rowsPerPage}
                                page={page}
                                onChangePage={this.handleChangePage}
                                onChangeRowsPerPage={this.handleChangeRowsPerPage}
                            />
                        </TableRow>
                    </TableFooter>
                </Table>
            </Paper>
        )
    }
}

export default withRouter(withStyles(styles)(TopicList))
