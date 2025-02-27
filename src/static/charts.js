function get_most_demanded_products(most_demanded_products_chart_labels, most_demanded_products_chart_dataValues, chart_color) {
    console.log(most_demanded_products_chart_labels, most_demanded_products_chart_dataValues)
    const most_demanded_products_chart = document.getElementById('most_demanded_products_chart');

    const most_demanded_products_chart_barColor = rootStyles.getPropertyValue('--pale-' + chart_color);
    const most_demanded_products_chart_borderColor = rootStyles.getPropertyValue('--dark-' + chart_color);

    new Chart(most_demanded_products_chart, {
        type: 'bar',
        data: {
            labels: most_demanded_products_chart_labels,
            datasets: [{
                label: null,
                data: most_demanded_products_chart_dataValues,
                borderWidth: 2,
                backgroundColor: most_demanded_products_chart_barColor,
                borderColor: most_demanded_products_chart_borderColor,
                minBarLength: 10,
            }]
        },
        options: {
            plugins: {
                legend: false
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
};

function get_most_popular_suppliers(most_popular_suppliers_chart_labels, most_popular_suppliers_chart_dataValues, chart_color) {
    console.log(most_popular_suppliers_chart_labels, most_popular_suppliers_chart_dataValues)
    const most_popular_suppliers_chart = document.getElementById('most_popular_suppliers_chart');

    const background_gray = rootStyles.getPropertyValue('--background-gray');

    const color1 = rootStyles.getPropertyValue('--pale-' + chart_color);
    const color2 = rootStyles.getPropertyValue('--main-' + chart_color);
    const color3 = rootStyles.getPropertyValue('--dark-' + chart_color);

    new Chart(most_popular_suppliers_chart, {
        type: 'doughnut',
        data: {
            labels: most_popular_suppliers_chart_labels,
            datasets: [{
                label: null,
                data: most_popular_suppliers_chart_dataValues,
                backgroundColor: [color2, color1, color3],
                borderColor: background_gray,
                borderWidth: 5,
                minBarLength: 10,
            }]
        },
        options: {
            plugins: {
                legend: false
            },
        }
    });
};

function get_most_popular_categories(most_popular_categories_chart_labels, most_popular_categories_chart_dataValues, chart_color) {
    console.log(most_popular_categories_chart_labels, most_popular_categories_chart_dataValues)
    const most_popular_categories_chart = document.getElementById('most_popular_categories_chart');

    const background_gray = rootStyles.getPropertyValue('--background-gray');

    const color1 = rootStyles.getPropertyValue('--pale-' + chart_color);
    const color2 = rootStyles.getPropertyValue('--main-' + chart_color);
    const color3 = rootStyles.getPropertyValue('--dark-' + chart_color);

    new Chart(most_popular_categories_chart, {
        type: 'doughnut',
        data: {
            labels: most_popular_categories_chart_labels,
            datasets: [{
                data: most_popular_categories_chart_dataValues,
                backgroundColor: [color2, color1, color3],
                borderColor: background_gray,
                borderWidth: 5,
                minBarLength: 10,
            }]
        },
        options: {
            plugins: {
                legend: false
            },
        }
    });
};