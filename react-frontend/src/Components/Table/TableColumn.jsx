export default function TableColumn({ children }) {
    return (
        <th scope="col" className="px-6 py-3 text-start whitespace-nowrap">
            <span className="text-xs font-semibold uppercase tracking-wide text-gray-800 dark:text-neutral-200">
                {children}
            </span>
        </th>
    )
}