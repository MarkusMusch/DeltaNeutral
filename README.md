# Funding Carry Dashboard

This Funding Carry Dashboard is a tool that collects real-time data from a cryptocurrency exchange, processes key metrics such as cumulative returns, and presents the insights in an interactive dashboard. Designed specifically for funding carry strategies, this app helps traders analyze performance, track funding rate differentials, and optimize their trading decisions.

<p align="center">
  <img src="https://github.com/MarkusMusch/DeltaNeutral/blob/main/images/BTC_cummulative_funding.png"
  width=50%>
</p>

## Includes:

The app follows a classical three-layer architecture that divides apps into three layers: the **Presentation Layer**, the **Logic Layer** and the **Data Access Layer**.

1. **The Presentation Layer: Data Analytics Dashboard**

- An interactive dashboard that visualizes key metrics such as cumulative returns and funding carry opportunities.

2. **The Logic Layer: Data Handling**

- Processes raw exchange data, computes funding carry metrics, and applies business logic.

3. **The Data Access Layer: Database and Data Access**

- Manages data retrieval, storage, and interaction with the crypto exchange API.

## Installation

First, clone the repository.

 ```bash
 git clone 'https://github.com/MarkusMusch/DeltaNeutral.git' && cd DeltaNeutral/
 ```

Second, install all necessary dependencies by calling:

 ```bash
 poetry install
 ```

## Usage

## Contributing

1. Fork it (https://github.com/MarkusMusch/DeltaNeutral/fork)
2. Create your feature branch (git checkout -b feature/fooBar)
3. Commit your changes (git commit -am 'Add some fooBar')
4. Push to the branch (git push origin feature/fooBar')
5. Create a new Pull Request

## License and author info

### Author

Markus Musch

### License

See the [LICENSE](LICENSE.txt) file for license rights and limitations (GNU GPLv3).