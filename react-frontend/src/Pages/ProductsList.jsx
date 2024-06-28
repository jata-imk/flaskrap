import Layout from "../Layouts/Layout";
import Table from "../Components/Table/Table";

import { useEffect, useState } from "react";
import { elements } from "chart.js";

export default function ProductsList({ products }) {
    const [productsWithCharts, setProductsWithCharts] = useState([]);

    useEffect(() => {
        console.log('Agregando graficas')
        setProductsWithCharts(products.map(product => {
            return {
                ...product,
                chart: {
                    options: {
                        plugins: {
                            legend: { display: false },
                            tooltip: { mode: 'nearest', intersect: false },
                        },
                        scales: {
                            y: { display: false },
                            x: { display: false }
                        },
                        elements: {
                            point: { radius: 0 }
                        },
                        maintainAspectRatio: false
                    },
                    data: {
                        labels: [
                            '25 January 2023',
                            '26 January 2023',
                            '27 January 2023',
                            '28 January 2023',
                            '29 January 2023',
                            '30 January 2023',
                            '31 January 2023',
                            '1 February 2023',
                            '2 February 2023',
                            '3 February 2023',
                            '4 February 2023',
                            '5 February 2023',
                            '6 February 2023',
                            '7 February 2023',
                            '8 February 2023',
                            '9 February 2023',
                            '10 February 2023',
                            '11 February 2023',
                            '12 February 2023',
                            '13 February 2023',
                            '14 February 2023'
                        ],
                        datasets: [
                            {
                                label: 'Precio',
                                data: Array.from({ length: 21 }, () => Math.floor(Math.random() * 100)),
                                borderColor: '#3b82f6',
                                borderWidth: 2,
                                tension: 0.1,
                            }
                        ]
                    },

                }
            }
        }));
    }, [products]);

    return (
        <div className="container">
            <Layout>
                <Table data={productsWithCharts}>
                    {{
                        title: "Vistazo general de productos",
                        subtitle: <>Dia a dia los precios de los productos cambian y es importante conocer su comportamiento para poder <span className="text-green-500">predecir</span> cuando es la época adecuada para adquirirlos</>
                    }}
                </Table>
            </Layout>
        </div>
    )
}