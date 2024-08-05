import { useContext } from "react";

import { TableContext } from "../../Context/TableContext"

export default function TableRow(props) {
    const { dynamicColumns } = useContext(TableContext);
    const { as, className, children, node, slots, classNames, state, ...otherProps } = props;

    const callback = otherProps?.callback;

    return (
        <tr className='bg-white hover:bg-gray-50 dark:bg-neutral-900 dark:hover:bg-neutral-800' >
            {callback
                ? dynamicColumns.map((item) => (
                    children(item.name)
                )) : children
            }
        </tr>
    );
};
