import React, { Component } from 'react'
import { Paper, Typography, Table, TableBody, TableRow, TableCell} from '@material-ui/core'
import { withStyles } from '@material-ui/core/styles'
import { withRouter } from 'react-router-dom'
import classNames from 'classnames'

import { FixedSpace } from 'components/Utils'

import { formatDate } from 'tools'

const styles = theme => {
    const colors = theme.palette
    return {
        header: {
            paddingTop: 10,
            paddingBottom: 10,
            paddingLeft: 25,
            paddingRight: 25,
            fontSize: '1.6em',
            fontWeight: 'bold',
            background: '#E9EAEC',
        },
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
        tableBodyRow: {
            paddingTop: 20,
            paddingBottom: 20,
            cursor: 'pointer',
            '& *': {
                color: colors.textPrimary.main,
            }
        },
        rowTitle: {
            fontWeight: 'bold',
            fontSize: '1.5em',
        },
        number: {
            fontWeight: 'bold',
            fontSize: '1.6em',
            textAlign: 'center',
        },
        rowSubtitle: {
            fontWeight: 500,
            textAlign: 'center',
        },
        rowTime: {
            fontWeight: 500,
        }
    }
}


class Category extends Component {

    handleRowClick = category => {
        this.props.history.push('/topics/?category=' + category.name)
    }

    render() {
        const { classes, categories } = this.props 
        return (
            <Paper className="paper">
                <FixedSpace size="xs3" className="paper-decorator"/>
                <Typography className={classNames(classes.tableTitle, classes.header)}>{this.props.title}</Typography>
                <Table>
                    <TableBody>
                        {categories.map((item, index) => {
                            return (
                                <TableRow hover className={classes.tableBodyRow} key={index} onClick={() => this.handleRowClick(item)}>
                                    <TableCell className={classNames(classes.titleColumn, classes.leftSpacing)}>
                                        <Typography className={classes.rowTitle}>{item.display_name}</Typography>
                                        <Typography>{item.desc}</Typography>
                                    </TableCell>
                                    <TableCell>
                                        <Typography className={classes.number}>{item.topics}</Typography>
                                        <Typography className={classes.rowSubtitle}>TOPICS</Typography>
                                    </TableCell>
                                    <TableCell>
                                        <Typography className={classes.number}>{item.posts}</Typography>
                                        <Typography className={classes.rowSubtitle}>POSTS</Typography>
                                    </TableCell>
                                    <TableCell>
                                        <Typography>{item.last_topic ? item.last_topic.title : ''}</Typography>
                                        <Typography className={classes.rowTime}>{item.last_topic ? formatDate(item.last_topic.date_submitted) : ''}</Typography> 
                                        <Typography>{item.last_topic ? 'by ' + item.last_topic.user.nickname : ''}</Typography>
                                    </TableCell>
                                </TableRow>
                            )
                        })}
                    </TableBody>
                </Table>
            </Paper>
        )
    }
}

export default withRouter(withStyles(styles)(Category))