const SearchBar = () => {
  return (
    <>
      <form action="" className="">
        <p className="text-red-500 text-center font-medium text-xs xl:text-[12px] mt-1">
          {}
        </p>
        <div className="flex items-center bg-[#E1ECE7] rounded-full shadow-lg px-3 sm:px-4 py-2 xl:w-xl mx-auto mt-2 mb-4">
          <input
            type="text"
            placeholder="Search for projects ....."
            className="flex-1 outline-none py-2 px-4 text-gray-700 placeholder-gray-400 text-sm sm:text-base min-w-0 border-b-0 rounded-full focus:border-b focus:border-b-[#00FFBB]"
          />
          <button className="bg-[#00FFBB] hover:bg-[#00fd7e] text-white px-3 sm:px-5 lg:px-4 py-2 rounded-full ml-2 transition-colors cursor-pointer text-xs sm:text-sm lg:text-base whitespace-nowrap">
            Search Project
          </button>
        </div>
      </form>
    </>
  );
};

export default SearchBar;
