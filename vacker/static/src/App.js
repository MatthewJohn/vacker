import React, { useState } from 'react';
import { Router, Route } from 'react-router-dom';
//import { connect } from 'react-redux';
import { createBrowserHistory } from 'history';

import {DataTable} from 'primereact/datatable';
import {Column} from 'primereact/column';

import 'primereact/resources/themes/nova-light/theme.css';
import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css';

import logo from './logo.svg';
import './App.css';

const history = createBrowserHistory();

// var state = {
//   searchValue: '',
//   enabled_columns: ['columnn', 'column2']
// }

var state_mapper = {};

function getStateValue(key) {
  return state_mapper[key]['getter'];
}

function setStateValue(key, value) {
  state_mapper[key]['setter'](value);
  // state[key] = value;
}


// function performSearch(search_value) {
    
// }

function onSearchChange(ev, force=false) {
  setStateValue('search_value', ev.target.value);
  if (ev.target.value.length >= 3 || force) {
    performSearch();
    console.log(ev.target.value);
  }
}

function performSearch() {
  console.log('searching for ' + getStateValue('search_value'));
  history.push("/search/" + getStateValue('search_value'));

  fetch('http://localhost:5000/search?query_string=' + getStateValue('search_value'))
    .then(response => response.json())
    .then(data => setStateValue('results', data['data']));
}




class SearchBar extends React.Component {

  onKeyDown = (e) => {
    if (e.key === 'Enter') {
      onSearchChange(e, true);
    }
  }

  onChange = (ev) => {
    onSearchChange(ev);
  }

  render() {
    return (<input type="text"
                   name="search_value"
                   value={getStateValue['search_value']}
                   onKeyDown={this.onKeyDown}
                   onChange={this.onChange} />);
  }
}




class ResultTable extends React.Component {

  constructor(props) {
    super(props);

    this.onVirtualScroll = this.onVirtualScroll.bind(this);
    this.state = {
      loading: true,
      results: getStateValue('results'),
      lazyTotalRecords: 20
    }
  }

  // getTableHeaders() {
  //   let headers = [];
  //   getStateValue('enabled_columns').forEach((col) => {
  //     headers.push(<th>{col}</th>);
  //   });
  //   return (
  //     <thead>
  //       <tr>
  //         {headers}
  //       </tr>
  //     </thead>
  //   );
  // }
  // render() {
  //   return (
  //     <table>
  //       {this.getTableHeaders()}
  //     </table>
  //   );
  // }





    loadChunk(index, length) {
      console.log(index);
      console.log(length);
        let chunk = [];
        for (let i = 0; i < length; i++) {
            chunk[i] = {...getStateValue('results')[i], ...{vin: (index + i)}};
        }

        return chunk;
    }

    onVirtualScroll(event) {
      console.log(event.first);
      console.log(event.rows);
      console.log(event);
        //for demo purposes keep loading the same dataset
        //in a real production application, this data should come from server by building the query with LazyLoadEvent options
        setTimeout(() => {
            //last chunk
            if (event.first === 249980) {
                this.setState({
                    results: this.loadChunk(event.first, 20)
                });
            }
            else {
                this.setState({
                    results: this.loadChunk(event.first, event.rows)
                });
            }
        }, 250);
    }

    loadingText() {
        return <span className="loading-text"></span>;
    }

    render() {
        return (
            <div>

                <div className="content-section introduction">
                    <div className="feature-intro">
                        <h1>DataTable - Scroll</h1>
                        <p>Data scrolling with fixed header is available horizontally, vertically or both. ScrollHeight and ScrollWidth values can either be fixed pixels or percentages. Certain columns can be fixed as well.
                            Virtual Scrolling mode is available to deal with large datasets by loading data on demand during scrolling.</p>
                    </div>
                </div>

                    <DataTable header="VirtualScroll with Lazy Loading" value={this.state.results} scrollable={true} scrollHeight="200px" virtualScroll={true} virtualRowHeight={30}
                        rows={20} totalRecords={this.state.lazyTotalRecords} lazy={true} onVirtualScroll={this.onVirtualScroll} style={{marginTop:'30px'}} loading={this.state.loading}>
                        <Column field="vin" header="Vin" loadingBody={this.loadingText} />
                        <Column field="year" header="Year" loadingBody={this.loadingText} />
                        <Column field="brand" header="Brand" loadingBody={this.loadingText} />
                        <Column field="color" header="Color" loadingBody={this.loadingText} />
                    </DataTable>
            </div>
        );
    }






}




class HomePage extends React.Component {

  render() {
    return (<div><SearchBar /></div>);
  }
}




class SearchPage extends React.Component {

  constructor(props) {
    super(props);
    setStateValue('search_value', this.props.match.params.search_value);
  }

  copmonentDidMount() {
    performSearch(this.props.match.params.search_value);
  }

  render() {
    return (
      <div>
        <SearchBar />
        <ResultTable />
      </div>);
  }
}




class FilePage extends React.Component {

  render() {
    return (<div></div>);
  }
}


class App extends React.Component {
    constructor(props) {
        super(props);

        const { dispatch } = this.props;
          history.listen((location, action) => {
        });
    }


    render() {
        const { alert } = this.props;
        return (

            <Router history={history}>
                <div>
                    <Route exact path="/" component={HomePage} />
                    <Route path="/search/:search_value" component={SearchPage} />
                    <Route path="/file/:file_id" component={FilePage} />
                </div>
            </Router>
        );
    }
}

function mapStateToProps(state) {
    const { alert } = state;
    return {
        alert
    };
}

//const connectedApp = connect(mapStateToProps)(App);
//export { connectedApp as App };


export default App;
