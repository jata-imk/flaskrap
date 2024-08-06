import Footer from "../Components/Footer";
import Navbar from "../Components/Navbar";

export default function Layout({ children }) {
    return (
        <>
            <Navbar />

            <main className="container mx-auto">
                {children}
            </main>
            
            <Footer />
        </>
    );
}