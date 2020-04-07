import React from 'react';
import { Router, Route, withRouter } from 'react-router-dom';
import { connect } from 'react-redux'
import { createBrowserHistory } from 'history';

import {DataTable} from 'primereact/datatable';
import {Column} from 'primereact/column';

import 'primereact/resources/themes/nova-light/theme.css';
import 'primereact/resources/primereact.min.css';
import 'primeicons/primeicons.css';

import logo from './logo.svg';
import './App.css';

const history = createBrowserHistory();


const mapStateToProps = (state) => {
   return {
      search_string: state.search_string,
      results: state.results,
      visible_results: state.visible_results,
      results_start: state.results_start,
      results_limit: state.results_limit,
      file_info: state.file_info,
      results_total: state.results_total,
      loading: state.loading
   };
};
const mapDispatchToProps = (dispatch) => {
   return {
      update_search_results: (res, total) => dispatch({
        type: 'UPDATE_RESULTS', res: res, records_total: total}),
      update_visible_results: (res, start, limit) => dispatch({
        type: 'UPDATE_VISIBLE_RESULTS', results: res, start: start, limit: limit}),

      update_search_string: (val) => dispatch({type: 'UPDATE_SEARCH', value: val}),
   };
};

class FunctionHolder extends React.Component {
  performSearch = () => {
    console.log('searching for ' + this.props.search_string);
    history.push("/search/" + this.props.search_string);

    fetch('http://localhost:5000/search?q=' + this.props.search_string)
      .then(response => response.json())
      .then(data => this.props.update_search_results(data['data'], data['recordsTotal']));
  }
}

class SearchBarBare extends FunctionHolder {

  constructor(props) {
    super(props);
    this.onSearchChange = this.onSearchChange.bind(this);
    this.performSearch = this.performSearch.bind(this);
  }

  onKeyDown = (e) => {
    if (e.key === 'Enter') {
      this.onSearchChange(e, true);
    }
  }

  onSearchChange(ev, force=false) {
    this.props.update_search_string(ev.target.value);
    if (ev.target.value.length >= 3 || force) {
      this.performSearch();
      console.log(ev.target.value);
    }
  }

  onChange = (ev) => {
    this.onSearchChange(ev);
  }

  render() {
    return (<input type="text"
                   name="search_string"
                   value={this.props.search_string}
                   onKeyDown={this.onKeyDown}
                   onChange={this.onChange} />);
  }
}

const SearchBar = connect(mapStateToProps, mapDispatchToProps)(SearchBarBare);




class ResultTableBare extends FunctionHolder {

  constructor(props) {
    super(props);

    this.onVirtualScroll = this.onVirtualScroll.bind(this);
    this.performSearch = this.performSearch.bind(this);
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
            chunk[i] = {...this.props.results[i], ...{vin: (index + i)}};
        }

        return chunk;
    }

    onVirtualScroll(event) {
      console.log(event.first);
      console.log(event.rows);
      console.log(event);
      this.props.update_visible_results(this.props.results, event.first, event.rows);
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

                    <DataTable header="VirtualScroll with Lazy Loading" value={this.props.visible_results} scrollable={true} scrollHeight="200px" virtualScroll={true} virtualRowHeight={30}
                        rows={20} totalRecords={this.props.results_total} lazy={true} onVirtualScroll={this.onVirtualScroll} style={{marginTop:'30px'}} loading={this.props.loading}>
                        <Column field="g_file_name" header="Filename" loadingBody={this.loadingText} />
                        <Column field="g_path" header="Path" loadingBody={this.loadingText} />
                        <Column field="g_size" header="File Size" loadingBody={this.loadingText} />
                        <Column field="g_file_type" header="Type" loadingBody={this.loadingText} />
                    </DataTable>
            </div>
        );
    }






}

const ResultTable = connect(mapStateToProps, mapDispatchToProps)(ResultTableBare);




class HomePage extends React.Component {

  render() {
    return (<div><SearchBar /></div>);
  }
}




class SearchPageBare extends React.Component {

  constructor(props) {
    super(props);
    this.props.update_search_string(this.props.match.params.search_string);
  }

  render() {
    return (
      <div>
        <SearchBar />
        <ResultTable />
      </div>);
  }
}

const SearchPage = connect(mapStateToProps, mapDispatchToProps)(SearchPageBare);




class FilePage extends React.Component {

  render() {
    return (<div></div>);
  }
}


class AppBare extends React.Component {
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
                    <Route path="/search/:search_string" component={SearchPage} />
                    <Route path="/file/:file_id" component={FilePage} />
                </div>
            </Router>
        );
    }
}

const App = connect(mapStateToProps)(AppBare);


export default App;
