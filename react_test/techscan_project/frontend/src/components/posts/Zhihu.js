import React, { Component, Fragment } from 'react';
import { connect } from 'react-redux';
import PropTypes from 'prop-types';
import { getZhihu, deleteZhihu } from '../../actions/zhihu';

export class Zhihu extends Component {
    static propTypes = {
        zhihu: PropTypes.array.isRequired
    };

    componentDidMount() {
        this.props.getZhihu();
    }

    render() {
        return (
        <Fragment>
            <h2>
                Zhihu
            </h2>
            <table className="table table-striped">
                <thead>
                    <tr>
                        <th>Id</th>
                        <th>Author</th>
                        <th>Summary</th>
                    </tr>
                </thead>
                <tbody>
                    { this.props.zhihu.map(zhihu => (
                        <tr key={zhihu.id}>
                            <td>
                                {zhihu.id}
                            </td>
                            <td>
                                {zhihu.author}
                            </td>
                            <td>
                                {zhihu.summary}
                            </td>
                            <td>
                                <button onClick={this.props.deleteZhihu.bind(this, zhihu.id)} className="btn btn-danger btn-sm">
                                    Delete
                                </button>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </Fragment>
        );
    }
}

const mapStateToProps = state => ({
    zhihu: state.zhihu.zhihu
});

export default connect(mapStateToProps, { getZhihu, deleteZhihu })(Zhihu);