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



      on_pagination_change: (start, limit) => dispatch({
        type: 'UPDATE_PAGINATION', start: start, limit: limit}),

      on_search_string_change: (val) => dispatch({
        type: 'UPDATE_SEARCH_STRING', value: val}),
   };
};

class FunctionHolder extends React.Component {
  perform_search_request = () => {
    console.log('searching for ' + this.props.search_string);
    console.log('start: ' + this.props.results_start + ', result limit: ' + this.props.results_limit);
    history.push("/search/" + this.props.search_string);

    fetch('http://localhost:5000/search?' + 
      'q=' + this.props.search_string +
      '&start=' + this.props.results_start +
      '&limit=' + this.props.results_limit)
      .then(response => response.json())
      .then(data => this.props.update_search_results(data['data'], data['recordsTotal']));
  }

  componentDidMount = () => {
    // On mount, check if search string is available.
    if (this.props.search_string) {
      this.perform_search_request();
    }
  }

  componentDidUpdate(prevProps, prevState, snapshot) {
    if (
        (prevProps.search_string !== this.props.search_string ||
          prevProps.results_limit !== this.props.results_limit ||
          prevProps.results_start !== this.props.results_start)
        && this.props.search_string) {
      this.perform_search_request();
    }
    // Temp hack
    //else {this.perform_search_request();}
  }
}

class SearchBarBare extends FunctionHolder {

  constructor(props) {
    super(props);
    this.onSearchChange = this.onSearchChange.bind(this);
  }

  onKeyDown = (e) => {
    if (e.key === 'Enter') {
      this.onSearchChange(e);
    }
  }

  onSearchChange(ev) {
    this.props.on_search_string_change(ev.target.value);
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
  }
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
      console.log(event);
      this.props.on_pagination_change(event.first, event.rows);
    }

    loadingText() {
      return <span className="loading-text"></span>;
    }

    render() {
        return (
            <div>

                <div className="content-section introduction">
                    <div className="feature-intro">
                        <h1>Results</h1>
                    </div>
                </div>

                    <DataTable value={this.props.results}
                            scrollable={true} scrollHeight="800px" virtualScroll={true}
                            virtualRowHeight={30} rows={50} totalRecords={this.props.results_total}
                            lazy={true} onVirtualScroll={this.onVirtualScroll}
                            style={{marginTop:'30px'}} loading={this.props.loading}>
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
    this.props.on_search_string_change(this.props.match.params.search_string);
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
