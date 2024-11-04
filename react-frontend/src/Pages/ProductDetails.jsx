import React from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

import { Button } from '@nextui-org/button';
import { Breadcrumbs, BreadcrumbItem } from '@nextui-org/breadcrumbs';
import { Avatar } from '@nextui-org/avatar';
import { Divider } from '@nextui-org/divider';
import { Dropdown, DropdownTrigger, DropdownMenu, DropdownItem } from '@nextui-org/dropdown';


import { FaDownload } from 'react-icons/fa';
import Layout from '../Layouts/Layout';
import AIPrompt from '../Components/AIPrompt';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const ProductDetail = ({ product }) => {
    // Prepare data for the chart
    const priceHistory = product.inventories[0].io_history
        .filter(history => history.io_type === 'PRICE_UPDATE')
        .sort((a, b) => new Date(a.transaction_date) - new Date(b.transaction_date));

    const chartData = {
        labels: priceHistory.map(history => new Date(history.transaction_date).toLocaleDateString()),
        datasets: [
            {
                label: 'Price History',
                data: priceHistory.map(history => parseFloat(history.price)),
                fill: false,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }
        ]
    };

    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: 'Product Price History',
            },
        },
    };

    // Assuming the download URL is constructed using the product's SKU
    const downloadUrl = `https://api.example.com/download-price-history/${product.sku}`;

    // Generate AI prompt based on price history
    const generateAIPrompt = () => {
        const seasons = ['Spring', 'Summer', 'Fall', 'Winter'];
        const pricesByMonth = priceHistory.reduce((acc, history) => {
            const month = new Date(history.transaction_date).getMonth();
            if (!acc[month]) acc[month] = [];
            acc[month].push(parseFloat(history.price));
            return acc;
        }, {});

        const averagePricesBySeason = seasons.map((season, index) => {
            const monthsInSeason = [index * 3, index * 3 + 1, index * 3 + 2];
            const pricesInSeason = monthsInSeason.flatMap(month => pricesByMonth[month] || []);
            const avgPrice = pricesInSeason.length ? pricesInSeason.reduce((sum, price) => sum + price, 0) / pricesInSeason.length : 0;
            return { season, avgPrice };
        });

        const bestSeason = averagePricesBySeason.reduce((best, current) =>
            current.avgPrice < best.avgPrice ? current : best
        );

        return `Based on historical prices, the best season to buy this product is ${bestSeason.season}.`;
    };

    const aiPrompt = generateAIPrompt();
    const providers = ['Supercolchones', 'Walmart', 'Chedraui'];
    const [selectedProvider, setSelectedProvider] = React.useState(providers[0]);

    return (
        <Layout currentPage="product">
            <div className="container mx-auto px-4 py-8 relative">
                <Breadcrumbs className="mb-4">
                    <BreadcrumbItem href="/">Inicio</BreadcrumbItem>
                    <BreadcrumbItem href="/productos">Productos</BreadcrumbItem>
                    <BreadcrumbItem>{product.name}</BreadcrumbItem>
                </Breadcrumbs>

                <h1 className="text-3xl font-bold mb-4">{product.name}</h1>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                    <div>
                        <img src={product.small_image || 'https://via.placeholder.com/150'} alt={product.name} className="w-full h-auto rounded-lg shadow-lg" />
                    </div>
                    <div>
                        <div className="flex flex-col md:flex-row gap-5 items-start mb-6">
                            <div className="flex items-center mb-4 md:mb-0">
                                <Avatar
                                    src="https://via.placeholder.com/40"
                                    size="md"
                                    className="mr-2"
                                />
                                <div>
                                    <p className="text-sm text-gray-500">Marca</p>
                                    <p className="font-semibold">Spring Air</p>
                                </div>
                            </div>
                            <div className="flex items-center">
                                <Avatar
                                    src="https://via.placeholder.com/40"
                                    size="md"
                                    className="mr-2"
                                />
                                <div>
                                    <p className="text-sm text-gray-500">Categoría</p>
                                    <p className="font-semibold">Camas y Colchones</p>
                                </div>
                            </div>
                        </div>
                        <div className="my-10">
                            <AIPrompt prompt={aiPrompt} />
                        </div>
                        <p className="text-xl mb-2"><strong>SKU:</strong> {product.sku}</p>
                        <p className="text-xl mb-2"><strong>Current Price:</strong> ${parseFloat(product.inventories[0].price).toFixed(2)}</p>
                        <p className="text-xl mb-2"><strong>Stock:</strong> {product.out_of_stock ? 'Out of Stock' : 'In Stock'}</p>
                        <p className="text-xl mb-4"><strong>Description:</strong> {product.description || 'No description available.'}</p>
                    </div>
                </div>
                <Divider className="my-8" />
                <div className="mt-8">
                    <div className="flex justify-between items-center mb-4">
                        <h2 className="text-2xl font-bold">Price History</h2>
                        <Button
                            as="a"
                            href={downloadUrl}
                            download
                            color="primary"
                            endContent={<FaDownload />}
                        >
                            Download Price History
                        </Button>
                    </div>
                    <div className="mb-6">
                        <Dropdown>
                            <DropdownTrigger>
                                <Button variant="bordered">
                                    {selectedProvider}
                                </Button>
                            </DropdownTrigger>
                            <DropdownMenu
                                aria-label="Select provider"
                                onAction={(key) => setSelectedProvider(key)}
                            >
                                {providers.map((provider) => (
                                    <DropdownItem key={provider}>
                                        {provider}
                                    </DropdownItem>
                                ))}
                            </DropdownMenu>
                        </Dropdown>
                    </div>
                    <div className="h-[400px] w-full">
                        <Line data={chartData} options={chartOptions} width={'100%'} />
                    </div>
                </div>
            </div>
        </Layout>
    );
};

export default ProductDetail;