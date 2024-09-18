import React, { useState } from "react";
import { useTable, useSortBy, useFilters, usePagination } from "react-table";
import {
  Container,
  Table,
  Button,
  Modal,
  ModalHeader,
  ModalBody,
  ModalFooter,
  Input,
} from "reactstrap";
import { FaEdit, FaTrash} from "react-icons/fa";
import {format} from "date-fns";
import { Filter, DefaultColumnFilter, SelectColumnFilter } from "./Filter";

const TableContainer = ({ columns, data, saveChanges, deleteEntry }) => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isModalDelOpen, setIsModalDelOpen] = useState(false);
  const [selectedRowData, setSelectedRowData] = useState(null);
  const [originalRowData, setOriginaldRowData] = useState(null);

  const toggleModal = () => setIsModalOpen(!isModalOpen);
  const toggleModalDel = () => setIsModalDelOpen(!isModalDelOpen);

  const handleEditRow = (rowData) => {
    let rowData_temp = { ...rowData };
    try{
      rowData_temp["date"] = format(rowData_temp["date"], "dd/MM");
      console.log(rowData["date"])
      console.log(rowData_temp["date"])
    } catch (error){}
    setOriginaldRowData(rowData_temp);
    setSelectedRowData(rowData_temp);
    toggleModal();
  };

  const handleDelRow = (rowData) => {
    let rowData_temp = { ...rowData };
    try{
      rowData_temp["date"] = format(rowData_temp["date"], "dd/MM");
      console.log(rowData["date"])
      console.log(rowData_temp["date"])
    } catch (error){}
    setOriginaldRowData(rowData_temp);
    setSelectedRowData(rowData_temp);
    toggleModalDel();
  };

  const handleInputChange = (e, key) => {
    setSelectedRowData({
      ...selectedRowData,
      [key]: e.target.value,
    });
  };

  const clickSave = () => {
    saveChanges(originalRowData, selectedRowData);
    toggleModal();
  };

  const clickDelete = () => {
    deleteEntry(selectedRowData);
    toggleModalDel();
  }

  const rankColumnExists = columns.some((col) => col.accessor === "rank");

  const initialSortBy = rankColumnExists
    ? [{ id: "rank", desc: false }]
    : [];

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    rows,
    prepareRow,
    state: { pageIndex, pageSize },
    setPageSize,
    canPreviousPage,
    canNextPage,
    pageOptions,
    gotoPage,
    nextPage,
    previousPage,
    setPageIndex,
    page,
  } = useTable(
    {
      columns,
      data,
      initialState: {
        pageIndex: 0,
        pageSize: 10,
        sortBy: initialSortBy,
      },
      defaultColumn: { Filter: DefaultColumnFilter },
    },
    useFilters,
    useSortBy,
    usePagination
  );

  const generateSortingIndicator = (column) => {
    return column.render("Header") === "Actions" ? " " : column.isSorted ? (column.isSortedDesc ? " 🔽" : " 🔼") : " ⇵";
  };

  const getRowClassName = (row) => {
    if (rankColumnExists) {
      const { rank } = row.original;
      return rank < 5 ? "highlight-row" : "";
    }
    return "";
  };

  return (
    <Container fluid style={{ marginTop: 20 }}>
      <Table bordered hover {...getTableProps()}>
        <thead>
          {headerGroups.map((headerGroup) => (
            <tr {...headerGroup.getHeaderGroupProps()}>
              {headerGroup.headers.map((column) => (
                <th {...column.getHeaderProps()}>
                  <div {...column.getSortByToggleProps()}>
                    {column.render("Header")}
                    {generateSortingIndicator(column)}
                  </div>
                  <Filter column={column} />
                </th>
              ))}
            </tr>
          ))}
        </thead>

        <tbody {...getTableBodyProps()}>
          {page.map((row) => {
            prepareRow(row);
            return (
              <tr {...row.getRowProps()} className={getRowClassName(row)}>
                {row.cells.map((cell) => (
                  <td {...cell.getCellProps()}>
                    {cell.render("Cell") === 'action_button' ? (
                      <><Button
                        color="primary"
                        onClick={() => handleEditRow(row.original)}
                      >
                        <FaEdit />
                      </Button><Button
                        color="secondary"
                        onClick={() => handleDelRow(row.original)}
                      >
                          <FaTrash />
                        </Button></>
                    ) : (
                      cell.render("Cell")
                    )}
                  </td>
                ))}
              </tr>
            );
          })}
        </tbody>
      </Table>

      <div className="pagination-container">
        <Button onClick={() => gotoPage(0)} disabled={!canPreviousPage}>
          {"<<"}
        </Button>{" "}
        <Button onClick={() => previousPage()} disabled={!canPreviousPage}>
          {"<"}
        </Button>{" "}
        <Button onClick={() => nextPage()} disabled={!canNextPage}>
          {">"}
        </Button>{" "}
        <Button
          onClick={() => gotoPage(pageOptions.length - 1)}
          disabled={!canNextPage}
        >
          {">>"}
        </Button>{" "}
        <span>
          Page{" "}
          <strong>
            {pageIndex + 1} of {pageOptions.length}
          </strong>{" "}
        </span>{" "}
        <select
          value={pageSize}
          onChange={(e) => setPageSize(Number(e.target.value))}
        >
          {[10, 20].map((size) => (
            <option key={size} value={size}>
              Show {size}
            </option>
          ))}
        </select>
      </div>
        
      {/* Edit Modal */}
      <Modal isOpen={isModalOpen} toggle={toggleModal}>
        <ModalHeader toggle={toggleModal}>Edit Row</ModalHeader>
        <ModalBody>
          {selectedRowData && (
            <div>
              {Object.keys(selectedRowData)
                .filter((key) => key !== 'id') // Exclude 'id' from being displayed
                .map((key) => (
                  <div key={key}>
                    <label>{key}:</label>
                    <Input
                      type="text"
                      value={String(selectedRowData[key])|| ''}
                      onChange={(e) => handleInputChange(e, key)} // Handle input change
                      style={{ marginBottom: '10px' }}
                    />
                  </div>
                ))}
            </div>
          )}
        </ModalBody>
        <ModalFooter>
          <Button color="secondary" onClick={toggleModal}>
            Cancel
          </Button>
          <Button color="primary" onClick={clickSave}>
            Save Changes
          </Button>
        </ModalFooter>
      </Modal>
        
      {/* Delete Modal */}
      <Modal isOpen={isModalDelOpen} toggle={toggleModalDel}>
        <ModalHeader toggle={toggleModalDel}>Delete Row</ModalHeader>
        <ModalBody>
          {selectedRowData && (
            <div>
            {Object.keys(selectedRowData)
              .filter((key) => key !== 'id') // Exclude 'id' from being displayed
              .map((key) => (
                <div key={key}>
                  <label>{key}:</label>
                  <span style={{ marginLeft: '10px' }}>{String(selectedRowData[key]) || 'N/A'}</span> {/* Display value without input */}
                </div>
              ))}
          </div>
          )}
        </ModalBody>
        <ModalFooter>
          <Button color="secondary" onClick={toggleModalDel}>
            Cancel
          </Button>
          <Button color="primary" onClick={clickDelete}>
            Delete
          </Button>
        </ModalFooter>
      </Modal>
    </Container>
  );
};

export default TableContainer;
