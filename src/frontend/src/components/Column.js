import { SelectColumnFilter } from "./Filter";
import { format } from "date-fns";

export const getColumnTeam = () => [
  {
    Header: "Name",
    accessor: "name",
  },
  {
    Header: "RegDate",
    accessor: "date",
    Cell: ({ value }) => {
      // Format date
      try{
      const date = new Date(value);
      return format(date, "dd/MM");
      } catch (error) {
        return value
      }
    },
  },
  {
    Header: "Group",
    accessor: "group",
    Filter: SelectColumnFilter,
  },
  {
    Header: "Actions", // This is where we add the edit icon
    Cell: "action_button",
    disableFilters: true, // Disable filtering for this column
    disableSortBy: true,  // Disable sorting for this column
  },
];

export const getColumnMatch = () => [
  {
    Header: "id",
    accessor: "id",
  },
  {
    Header: "Home",
    accessor: "team_one",
  },
  {
    Header: "Away",
    accessor: "team_two",
  },
  {
    Header: "Home Goals",
    accessor: "goal_one",
  },
  {
    Header: "Away Goals",
    accessor: "goal_two",
  },
  {
    Header: "Actions", // This is where we add the edit icon
    Cell: "action_button",
    disableFilters: true, // Disable filtering for this column
    disableSortBy: true,  // Disable sorting for this column
  },
];

export const getColumnResult = () => [
  {
    Header: "id",
    accessor: "id",
  },
  {
    Header: "Rank",
    accessor: "rank",
  },
  {
    Header: "Name",
    accessor: "name",
  },
  {
    Header: "Goals",
    accessor: "goal",
  },
  {
    Header: "Games Played",
    accessor: "game",
    Filter: SelectColumnFilter,
  },
];
