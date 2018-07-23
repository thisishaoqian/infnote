import React, { Component } from 'react'
import { Route } from 'react-router-dom'
import { TopicListPage, TopicPage } from 'components/Topic'
import { CategoryPage } from 'components/Category'
import { FixedSpace } from 'components/Utils'
import { UserInfo } from 'components/User'
import Navbar from './Navbar'
import { Alert } from '../Utils'


class App extends Component {
    render() {
        return (
            <div className="app">
                <Navbar />
                <Alert />
                <FixedSpace size="xl"/>
                <Route exact path="/" component={CategoryPage}/>
                <Route exact path="/topics/" component={TopicListPage}/>
                <Route exact path="/topic/:id" component={TopicPage}/>
                <Route exact path="/userinfo/" component={UserInfo}/>
            </div>
        )
    }
}

export default App
