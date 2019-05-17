import React, { Component } from 'react'

export class Header extends Component {
  render() {
    return (
        <nav className="navbar navbar-expand-lg navbar-light bg-light">
          <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarTogglerDemo01" aria-controls="navbarTogglerDemo01" aria-expanded="false" aria-label="Toggle navigation">
            <span className="navbar-toggler-icon"></span>
          </button>
          <div>
            <a className="navbar-brand" href="#">TechScan China</a>
          </div>
          <form action="/zhihu" method="get">
            <div class="md-form mt-0">
              <input class="form-control" type="text" placeholder="Search" aria-label="Search" name="summary__contains"></input>
            </div>
          </form>
        </nav>
    )
  }
}

export default Header