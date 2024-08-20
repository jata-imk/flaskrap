import Layout from "../Layouts/Layout";

import { useEffect, useState, useCallback, useMemo } from "react";

import { DatePicker } from "@nextui-org/date-picker";
import { Pagination } from "@nextui-org/pagination";
import { Input } from "@nextui-org/input";
import {
    Table, TableHeader, TableColumn, TableBody, TableRow, TableCell
} from "@nextui-org/table";

import { MdInfoOutline } from "react-icons/md";
import { Tooltip as TooltipNext } from "@nextui-org/tooltip";
import { Button } from "@nextui-org/button";

import { now, getLocalTimeZone } from "@internationalized/date";

import { columns } from "../Config/productsListConfig";

import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
} from 'chart.js';

import { Line } from 'react-chartjs-2';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);


export default function ProductsList({ products }) {
    const [filterValue, setFilterValue] = useState("");
    const [dateFilter, setDateFilter] = useState(null);
    const [page, setPage] = useState(1);
    const [pages, setPages] = useState(0);
    const rowsPerPage = 5;

    const hasSearchFilter = Boolean(filterValue);

    const filteredProducts = useMemo(() => {
        let filteredProducts = [...products];

        if (hasSearchFilter) {
            filteredProducts = filteredProducts.filter((product) =>
                product.name.toLowerCase().includes(filterValue.toLowerCase()),
            );
        }

        // if (dateFilter) {
        //     filteredProducts = filteredProducts.filter((user) =>
        //         user.created_at.toISOString().split("T")[0] === dateFilter.toISOString().split("T")[0]
        //     );
        // }

        setPages(Math.ceil(filteredProducts.length / rowsPerPage));

        return filteredProducts;
    }, [products, filterValue]);

    const paginatedProducts = useMemo(() => {
        const start = (page - 1) * rowsPerPage;
        const end = start + rowsPerPage;

        return filteredProducts.slice(start, end);
    }, [page, filteredProducts]);

    const renderCell = useCallback((product, columnKey) => {
        const cellValue = product[columnKey];

        switch (columnKey) {
            case "id":
                return (
                    <button type="button" className="flex items-center gap-x-2">
                        <svg className="flex-shrink-0 size-4 text-gray-800 dark:text-white" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" /></svg>
                        <span className="text-sm text-gray-800 dark:text-neutral-200">{cellValue}</span>
                    </button>
                );
            case "name":
                return (
                    <div className="flex items-center gap-x-3">
                        <div className="w-15">
                            <img src={`https://picsum.photos/id/${product.id * 4}/40`} alt="Lorem ipsum img" />
                        </div>
                        <div className="flex flex-col">
                            <span className="font-semibold text-sm text-gray-800 dark:text-white">{product.name}</span>
                            <span className="text-xs text-gray-500 dark:text-neutral-500">{product.sku}</span>
                        </div>
                    </div>
                );
            case "price":
                const priceFormatted = new Intl.NumberFormat('es-MX', { style: 'currency', currency: 'MXN' }).format(product.inventories[0].price);
                return (
                    <span className="text-sm text-gray-800 dark:text-white">{priceFormatted}</span>
                );
            case "last_7d":
                let product_inventories_io_history = [...product?.inventories[0]?.io_history];

                if (product_inventories_io_history.length == 0 || product_inventories_io_history.length < 21) {
                    return (
                        <TooltipNext content="No hay suficientes datos para mostrar este indicador">
                            <Button className="bg-transparent">
                                <MdInfoOutline />
                            </Button>
                        </TooltipNext>
                    )
                }

                const firstSevenIOHistoryItems = product_inventories_io_history.slice(0, 7);
                let averageFirstSevenIOHistoryItems = firstSevenIOHistoryItems.reduce((a, b) => Number(a) + Number(b.price), 0) / firstSevenIOHistoryItems.length;

                const nextFourteenIOHistoryItems = product_inventories_io_history.slice(7, 14);
                let averageNextFourteenIOHistoryItems = nextFourteenIOHistoryItems.reduce((a, b) => Number(a) + Number(b.price), 0) / firstSevenIOHistoryItems.length;

                const percentageChange = (averageNextFourteenIOHistoryItems / averageFirstSevenIOHistoryItems) - 1;
                const percentageChangeFormatted = Number(percentageChange).toLocaleString("es-MX", { style: "percent", minimumFractionDigits: 2 });
                console.log(averageFirstSevenIOHistoryItems, averageNextFourteenIOHistoryItems, percentageChange);
                let fontColor = percentageChange == 0 ? "text-gray-500" : (percentageChange > 0 ? "text-red-500" : "text-green-500");

                return (
                    <span className={"text-sm ".concat(fontColor)}>{percentageChangeFormatted}</span>
                )
            case "last_21d":
                let io_history = [...product?.inventories[0]?.io_history];

                if (io_history.length < 21) {
                    io_history = [
                        ...Array(21 - io_history.length).fill({
                            price: null,
                            transaction_date: null
                        }), ...io_history
                    ];
                }

                if (io_history.length == 0) {
                    return <div className="text-gray-400 dark:text-white italic" style={{ height: '75px', lineHeight: '75px' }}>Sin información reciente</div>;
                }

                const chart = {
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
                        labels: io_history.map((price_history_item) => {
                            const fechaObj = new Date(price_history_item.transaction_date);
                            const opciones = {
                                weekday: 'long',
                                year: 'numeric',
                                month: 'long',
                                day: 'numeric'
                            };

                            return fechaObj.toLocaleDateString('es-MX', opciones);
                        }),
                        datasets: [
                            {
                                label: 'Precio',
                                data: io_history.map((io_history_item) => io_history_item.price),
                                borderColor: '#3b82f6',
                                borderWidth: 2,
                                tension: 0.1,
                            }
                        ]
                    }
                };

                return (
                    <div className="inline-block">
                        <Line
                            options={chart.options}
                            data={chart.data}
                            width={175}
                            height={75}
                        />
                    </div>
                );
            default:
                return cellValue;
        }
    }, []);

    useEffect(() => {
        if (dateFilter === null || dateFilter === undefined) {
            setDateFilter(now(getLocalTimeZone()));
        }
    }, []);

    const onSearchChange = useCallback((value) => {
        if (value) {
            setFilterValue(value);
            setPage(1);
        } else {
            setFilterValue("");
        }
    }, []);

    const onClear = useCallback(() => {
        setFilterValue("")
        setPage(1)
    }, [])

    return (
        <Layout currentPage={'products'}>
            <div className="flex flex-col items-end	w-full flex-wrap md:flex-nowrap gap-4  my-4">
                <DatePicker
                    value={dateFilter}
                    granularity="day"
                    onChange={setDateFilter}
                    maxValue={now(getLocalTimeZone())}
                    label="Fecha de corte para los precios"
                    className="max-w-[284px]"
                    description={"Es la fecha a partir de la cual se leeran los precios de la base de datos hasta 21 dias antes"}
                />

                <Input
                    isClearable
                    className="w-full sm:max-w-[44%]"
                    placeholder="Buscar por nombre..."
                    value={filterValue}
                    onClear={() => onClear()}
                    onValueChange={onSearchChange}
                />
            </div>

            <Table className="min-w-full divide-y divide-gray-200 dark:divide-neutral-700"
                aria-label="Listado de productos que han sido agregado al sistema"
                selectionMode="multiple"
                topContent={
                    <div className="px-6 py-4 border-b border-gray-200 dark:border-neutral-700">
                        <h2 className="text-xl font-semibold text-gray-800 dark:text-neutral-200">
                            Vistazo general de productos
                        </h2>
                        <p className="text-sm text-gray-600 dark:text-neutral-400">
                            Dia a dia los precios de los productos cambian y es importante conocer su comportamiento para poder predecir cuando es la época adecuada para adquirirlos
                        </p>
                    </div>
                }
                bottomContent={
                    <div className="flex w-full justify-center">
                        <Pagination
                            isCompact
                            showControls
                            showShadow
                            color="secondary"
                            page={page}
                            total={pages}
                            onChange={(page) => setPage(page)}
                        />
                    </div>
                }
            >
                <TableHeader className="bg-gray-50 dark:bg-neutral-800" columns={columns}>
                    {(column) => (
                        <TableColumn className="px-6 py-3 text-start whitespace-nowrap" key={column.uid} align={column.uid === "actions" ? "center" : "start"}>
                            {column.name}
                        </TableColumn>
                    )}
                </TableHeader>
                <TableBody items={paginatedProducts}>
                    {(item) => (
                        <TableRow className="bg-white hover:bg-gray-50 dark:bg-neutral-900 dark:hover:bg-neutral-800 " key={item.id}>
                            {(columnKey) => <TableCell>{renderCell(item, columnKey)}</TableCell>}
                        </TableRow>
                    )}
                </TableBody>
            </Table>
        </Layout>
    )
}