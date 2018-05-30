import React, { Component } from 'react'
import { Route } from 'react-router-dom'
import { TopicListPage, TopicPage } from 'components/Topic'
import { FixedSpace } from 'components/Utils'
import Navbar from './Navbar'

class App extends Component {
    render() {
        return (
            <div className="app">
                <Navbar />
                <FixedSpace size="xl"/>
                <Route path="/topic/list" component={TopicListPage}/>
                <Route exact path="/topic" component={TopicPage}/>
            </div>
        )
    }
}

export default App
