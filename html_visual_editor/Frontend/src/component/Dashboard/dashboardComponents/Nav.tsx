import { Link } from "react-router-dom";
import Logo from "../../../assets/logo.png";
import type React from "react";

type NavProps = {
  setUploadImg: React.Dispatch<React.SetStateAction<boolean>>;
};

const Nav: React.FC<NavProps> = ({ setUploadImg }) => {
  return (
    <nav className="sticky top-0 z-50 flex justify-center backdrop-blur-xl border-b border-white/10 shadow-lg bg-[#1C1B18]">
      <div className="w-full lg:w-[calc(100vw-15rem)] h-15 flex justify-between items-center px-3 ">
        <div className="flex justify-center items-center  gap-2 text-xl ">
          <img src={Logo} alt="logo" className="w-7" />
          <h1 className="text-white font-bold">
            <div className="flex">
              <Link to="/" className="text-xs lg:text-2xl">
                Precision<span className="text-[#00FFBB]">Docx</span>
              </Link>
            </div>
          </h1>
        </div>
        <button
          className=" font-bold text-[13px] border border-2 border-[#00FFBB] text-[#00FFBB] w-30 h-7 rounded-xl duration-300 hover:border-none hover:bg-transparent cursor-pointer"
          onClick={() => setUploadImg(true)}
        >
          Add Project
        </button>
      </div>
    </nav>
  );
};

export default Nav;
