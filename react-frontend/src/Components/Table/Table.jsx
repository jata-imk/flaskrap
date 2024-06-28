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

export default function Table({ data, children }) {
    return (
        <div className="max-w-[85rem] px-4 py-10 sm:px-6 lg:px-8 lg:py-14 mx-auto">
            <div className="flex flex-col">
                <div className="-m-1.5 overflow-x-auto">
                    <div className="p-1.5 min-w-full inline-block align-middle">
                        <div className="bg-white border border-gray-200 rounded-xl shadow-sm overflow-hidden dark:bg-neutral-900 dark:border-neutral-700">
                            {(children && (children.hasOwnProperty('title') || children.hasOwnProperty('subtitle'))) &&
                                <div className="px-6 py-4 border-b border-gray-200 dark:border-neutral-700">
                                    <h2 className="text-xl font-semibold text-gray-800 dark:text-neutral-200">
                                        {children.title}
                                    </h2>
                                    <p className="text-sm text-gray-600 dark:text-neutral-400">
                                        {children.subtitle}
                                    </p>
                                </div>
                            }

                            <table className="min-w-full divide-y divide-gray-200 dark:divide-neutral-700">
                                <thead className="bg-gray-50 dark:bg-neutral-800">
                                    <tr>
                                        <th scope="col" className="px-6 py-3 text-start whitespace-nowrap">
                                            <span className="text-xs font-semibold uppercase tracking-wide text-gray-800 dark:text-neutral-200">
                                                #
                                            </span>
                                        </th>

                                        <th scope="col" className="px-6 py-3 text-start whitespace-nowrap min-w-64">
                                            <span className="text-xs font-semibold uppercase tracking-wide text-gray-800 dark:text-neutral-200">
                                                Nombre
                                            </span>
                                        </th>

                                        <th scope="col" className="px-6 py-3 text-start whitespace-nowrap">
                                            <span className="text-xs font-semibold uppercase tracking-wide text-gray-800 dark:text-neutral-200">
                                                Precio
                                            </span>
                                        </th>

                                        <th scope="col" className="px-6 py-3 text-start whitespace-nowrap">
                                            <span className="text-xs font-semibold uppercase tracking-wide text-gray-800 dark:text-neutral-200">
                                                7d
                                            </span>
                                        </th>

                                        <th scope="col" className="px-6 py-3 text-start whitespace-nowrap">
                                            <span className="text-xs font-semibold uppercase tracking-wide text-gray-800 dark:text-neutral-200">
                                                Últimos 21 días
                                            </span>
                                        </th>
                                    </tr>
                                </thead>

                                <tbody className="divide-y divide-gray-200 dark:divide-neutral-700">
                                    {data.map((product, index) => {
                                        return <tr key={product.sku} className='bg-white hover:bg-gray-50 dark:bg-neutral-900 dark:hover:bg-neutral-800 '>
                                            <td className="size-px whitespace-nowrap px-6 py-3">
                                                <button type="button" className="flex items-center gap-x-2">
                                                    <svg className="flex-shrink-0 size-4 text-gray-800 dark:text-white" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" /></svg>
                                                    <span className="text-sm text-gray-800 dark:text-neutral-200">{index + 1}</span>
                                                </button>
                                            </td>
                                            <td className="size-px whitespace-nowrap px-6 py-3">
                                                <div className="flex items-center gap-x-3">
                                                    <div className="w-5">
                                                        <img src={`https://picsum.photos/id/${product.id * 4}/40`} alt="Lorem ipsum img" />
                                                    </div>
                                                    <span className="font-semibold text-sm text-gray-800 dark:text-white">{product.name}</span>
                                                    <span className="text-xs text-gray-500 dark:text-neutral-500">BTC</span>
                                                </div>
                                            </td>
                                            <td className="size-px whitespace-nowrap px-6 py-3">
                                                <span className="text-sm text-gray-800 dark:text-white">$26,869.14</span>
                                            </td>
                                            <td className="h-px w-72 whitespace-nowrap">
                                                <span className="text-sm text-red-500">-3.8%</span>
                                            </td>
                                            <td className="size-px whitespace-nowrap px-6 py-3">
                                                <div className="inline-block">
                                                    <Line
                                                        options={ product.chart.options }
                                                        data={ product.chart.data }
                                                        width={150}
                                                        height={50}
                                                    />
                                                </div>
                                            </td>
                                        </tr>
                                    })}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}