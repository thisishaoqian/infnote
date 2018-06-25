import React, { Component } from 'react'
import { Route } from 'react-router-dom'
import { TopicListPage, TopicPage } from 'components/Topic'
import { CategoryPage } from 'components/Category'
import { FixedSpace } from 'components/Utils'
import Navbar from './Navbar'


class App extends Component {
    render() {
        return (
            <div className="app">
                <Navbar />
                <FixedSpace size="xl"/>
                <Route exact path="/" component={CategoryPage}/>
                <Route exact path="/topics/" component={TopicListPage}/>
                <Route exact path="/topic/:id" component={TopicPage}/>
            </div>
        )
    }
}

export default App
