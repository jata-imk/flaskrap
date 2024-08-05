export default function Button( { children, startContent, endContent, ...props } ) {
    return (
        <button type="button" class="py-3 px-4 flex justify-center items-center size-[46px] text-sm font-semibold rounded-lg border border-transparent bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50 disabled:pointer-events-none">
            {startContent} {children} {endContent}
        </button>
    )
}