import Footer from "../Components/Footer";
import Navbar from "../Components/Navbar";

export default function Layout({ currentPage, children }) {
    return (
        <>
            <Navbar currentPage={currentPage} />

            <main className="container mx-auto">
                {children}
            </main>
            
            <Footer />
        </>
    );
}