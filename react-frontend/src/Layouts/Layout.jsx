import Footer from "../Components/Footer";
import Navbar from "../Components/Navbar";

export default function Layout({ children }) {
    return (
        <>
            <Navbar />

            <main>
                {children}
            </main>
            
            <Footer />
        </>
    );
}