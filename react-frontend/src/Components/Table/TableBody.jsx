export default function TableBody(props) {
    const { as, className, children, node, slots, classNames, state, ...otherProps } = props;

    return (
        <tbody className="divide-y divide-gray-200 dark:divide-neutral-700">
            {otherProps?.items && otherProps.items.map((row) => (
                children(row)
            ))}

            {!otherProps?.items && children}
        </tbody>
    )
}