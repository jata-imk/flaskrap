export default function TableHeader(props) {
    const { as, className, children, node, slots, classNames, state, ...otherProps } = props;

    return (
        <thead className="bg-gray-50 dark:bg-neutral-800">
            <tr>
                {otherProps?.columns && otherProps.columns.map((column) => (
                    children(column)
                ))}

                {!otherProps?.columns && children}
            </tr>
        </thead>
    );
}