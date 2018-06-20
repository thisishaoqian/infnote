import React, { Component } from 'react'
import { withRouter } from 'react-router'
import { withStyles } from '@material-ui/core/styles'
import { Redirect } from 'react-router-dom'
import classNames from 'classnames'
import { Paper, Typography, Table, TableBody, TableCell, TableHead, TableFooter, TablePagination, TableRow } from '@material-ui/core'
import { Post, Store } from 'models'
import { formatDate } from 'tools'


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
            cursor: 'pointer',
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
        Post.retrieveList(this.props.category).then(data => {
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
                                    <TableCell>{item.user.nickname}</TableCell>
                                    <TableCell>{item.replies}</TableCell>
                                    <TableCell>{item.last_reply ? formatDate(item.last_reply.date_submitted) : formatDate(item.date_submitted)}<br />by {item.last_reply ? item.last_reply.user.nickname : item.user.nickname}</TableCell>
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
