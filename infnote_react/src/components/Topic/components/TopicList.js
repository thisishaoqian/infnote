import React, { Component } from 'react'
import { withRouter } from 'react-router'
import { withStyles } from '@material-ui/core/styles'
import classNames from 'classnames'
import { Paper, Typography, Table, TableBody, TableCell, TableHead, TableFooter, TablePagination, TableRow } from '@material-ui/core'
import { TopicData } from 'components/Test'
import { FixedSpace } from 'components/Utils'

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
            rowsPerPage: 10,
            page: 0,
        }
    }

    handleChangePage = (event, page) => {
        this.setState({ page })
    }

    handleChangeRowsPerPage = (event) => {
        this.setState({ rowsPerPage: event.target.value })
    }

    render() {
        const { classes } = this.props
        const { rowsPerPage, page} = this.state
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
                        {TopicData.slice(page * rowsPerPage, (page + 1) * rowsPerPage).map((item, index) => {
                            return (
                                <TableRow key={index} className={classes.tableBodyRow}>
                                    <TableCell className={classNames(classes.titleColumn, classes.leftSpacing)}>
                                        {item.title}
                                    </TableCell>
                                    <TableCell>{item.author}</TableCell>
                                    <TableCell>{item.replies}</TableCell>
                                    <TableCell>Today 03:32:54 am<br />by {item.last}</TableCell>
                                </TableRow>
                            )
                        })}
                    </TableBody>
                    <TableFooter>
                        <TableRow>
                            <TablePagination 
                                count={TopicData.length}
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
