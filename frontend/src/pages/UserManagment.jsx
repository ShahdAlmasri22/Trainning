import {
    Button,
    Box,
    Typography,
    Table,
    TableHead,
    TableRow,
    TableCell,
    TableBody,
    Paper,
    TableContainer, Dialog, DialogTitle, DialogContent, DialogActions, FormControl, InputLabel, Select, MenuItem,
    TextField, CircularProgress, Alert, Snackbar
} from "@mui/material";
import {useEffect, useState} from "react";
import { useNavigate } from "react-router-dom";
import { useQuery, useQueryClient, useMutation } from "@tanstack/react-query";
import UsersLogsTable from "../components/UsersLogsTable.jsx";
import ChangeRoleDialog from "../components/ChangeRoleDialog.jsx";
import Pagging from "../components/PaggingUserLog.jsx";
import PaggingUserLog from "../components/PaggingUserLog.jsx";
import DeleteUserDialog from "../components/DeleteUserDialog.jsx";
import Toast from "../components/Toast.jsx";


function UserManagment() {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState("users");
  const baseURL = import.meta.env.VITE_BACK_URL;

  const [openRoleDialog, setOpenRoleDialog] = useState(false);
  const [selectedUser, setSelectedUser] = useState(null);
  const [newRole, setNewRole] = useState("");

  const [searchKey, setSearchKey] = useState("");

  const [openDeleteDialog, setOpenDeleteDialog] = useState(false);
  const [userToDelete, setUserToDelete] = useState(null);

  const queryClient = useQueryClient();

  const [page, setPage] = useState(1);
  const limit = 10;

  const [toast, setToast] = useState({
    open: false,
    message: "",
    severity:  "error" | "success" | "warning" | "info",
  });

  const toastSuccess = (msg) =>
  setToast({ open: true, message: msg, severity: "success" });

  const toastError = (msg) =>
  setToast({ open: true, message: msg, severity: "error" });


  const refreshAccessToken = useMutation({
    mutationFn: async () => {
      const refresh_token = localStorage.getItem("refresh_token");

      if (!refresh_token) {
        throw new Error("No refresh token");
      }

      const res = await fetch(`${baseURL}/users/refresh`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${refresh_token}`,
        },
      });

      const data = await res.json();

      if (!res.ok || !data.access_token) {
        throw new Error("Refresh failed");
      }

      return data.access_token;
    },

    onSuccess: (newToken) => {
      localStorage.setItem("access_token", newToken);
    },

    onError: () => {
      localStorage.clear();
      window.location.href = "/users/login";
    },
  });

    const fetchWithAuth = async (url, options = {}) => {
    let token = localStorage.getItem("access_token");

    let res = await fetch(url, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
        ...options.headers,
      },
    });

    if (res.status === 401) {
      try {
        token = await refreshAccessToken.mutateAsync();

        res = await fetch(url, {
          ...options,
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
            ...options.headers,
          },
        });
      } catch (err) {
        throw new Error("Unauthorized");
      }
    }

    if (!res.ok) {
      let errMessage = "Something went wrong";

      try {
        const err = await res.json();
        errMessage = err.message || err.detail || errMessage;
      } catch (e) {}

      throw new Error(errMessage);
    }

    return res.json();
  };

  const { data: usersData, isLoading: usersLoading } = useQuery({
      queryKey: ["users"],
      queryFn: () => fetchWithAuth(`${baseURL}/users/view`),
      enabled: activeTab === "users" && !searchKey,
  });

  const { data: logsData, isLoading: logsLoading } = useQuery({
      queryKey: ["logs"],
      queryFn: () => fetchWithAuth(`${baseURL}/logged/view`),
      enabled: activeTab === "logs" && !searchKey,
      onError: (err) => {
        toastError(err.message);
      },
  });


  const handleUpdateRole = () => {
      updateRoleMutation.mutate({
        userId: selectedUser.ID,
        newRole,
      });
  };

  const handleOpenRoleDialog = (user) => {
      setSelectedUser(user);
      setNewRole(user.role);
      setOpenRoleDialog(true);
  };

  const handleClose = () => {
      setOpenRoleDialog(false);
      setSelectedUser(null);
      setNewRole("");
  };

  const updateRoleMutation = useMutation({
      mutationFn: ({ userId, newRole }) => {
        return fetchWithAuth(
          `${baseURL}/users/role/${userId}?new_role=${newRole}`,
          {
            method: "PATCH",
          }
        );
      },

      onSuccess: () => {
        queryClient.invalidateQueries({ queryKey: ["users"] })
        handleClose();
        toastSuccess("Role created successfully ✅");
      },
      onError: (err) => {
        toastError(err.message);
      },
  });

  const deleteUserMutation = useMutation({
      mutationFn: (userId) => {
        return fetchWithAuth(`${baseURL}/users/${userId}`, {
          method: "DELETE",
        });
      },

      onSuccess: () => {
        queryClient.invalidateQueries({ queryKey: ["users"] });
        toastSuccess("User deleted successfully ✅");

      },
      onError: (err) => {
        toastError(err.message);
      },
  });

  const handleDeleteUser = (userId) => {
      setUserToDelete(userId);
      setOpenDeleteDialog(true);
  };

  const confirmDeleteUser = () => {
      deleteUserMutation.mutate(userToDelete);
      setOpenDeleteDialog(false);
      setUserToDelete(null);
  };


  const { data: searchData, isLoading: searchLoading } = useQuery({
      queryKey: ["search", searchKey, activeTab, page],
      queryFn: () => {
        if (activeTab === "users") {
          return fetchWithAuth(
            `${baseURL}/users/search?key=${searchKey}`
          );
        } else {
          return fetchWithAuth(
            `${baseURL}/logged/search?key=${searchKey}`
          );
        }
      },
      onError: (err) => {
        toastError(err.message);
      },
      enabled: searchKey.trim().length > 0,
    });

  useEffect(() => {
      setPage(1);
    }, [searchKey, activeTab]);

  const allUsers =
    activeTab === "users"
    ? (searchKey ? searchData?.users : usersData?.users) || []
    : [];

  const allLogs =
    activeTab === "logs"
    ? (searchKey ? searchData?.result : logsData?.result) || []
    : [];

  const isLoading =
   searchKey.trim().length > 0 ? searchLoading : usersLoading;

  const startIndex = (page - 1) * limit;
  const endIndex = startIndex + limit;

  const users = allUsers.slice(startIndex, endIndex);
  const logs = allLogs.slice(startIndex, endIndex);

  const totalUsersPages = Math.ceil(allUsers.length / limit);
  const totalLogsPages = Math.ceil(allLogs.length / limit);

  const totalPages =
   activeTab === "users" ? totalUsersPages : totalLogsPages;

  return (
    <Box>
      <Typography
        sx={{
          textAlign: "center",
          mt: 3,
          fontWeight: "bold",
          fontSize: "28px",
          color: "#472661",
        }}
      >
        User Management
      </Typography>

      <Button
        variant="contained"
        onClick={() => navigate("/tasks")}
        sx={{
          textTransform: "none",
          borderRadius: 3,
          px: 2.5,
          py: 0.5,
          fontSize: "12px",
          ml: 3,
          mt: 3,
          background: "#472661",
        }}
      >
        ← Back to task page
      </Button>

      <Box sx={{ display: "flex", justifyContent: "center", mt: 3, gap: 2 }}>
        <Button
          onClick={() => {setActiveTab("users"); setSearchKey("");}}
          sx={{
            borderRadius: 3,
            fontSize: "12px",
            background: activeTab === "users" ? "#472661" : "#e0e0e0",
            color: activeTab === "users" ? "white" : "black",
            "&:hover": {
              background: "#472661",
              color: "white",
            },
          }}
        >
          Users
        </Button>

        <Button
          onClick={() => {setActiveTab("logs"); setSearchKey("");}}
          sx={{
            borderRadius: 3,
            fontSize: "12px",
            background: activeTab === "logs" ? "#472661" : "#e0e0e0",
            color: activeTab === "logs" ? "white" : "black",
            "&:hover": {
              background: "#472661",
              color: "white",
            },
          }}
        >
          Logged
        </Button>
      </Box>

    <TextField
      margin="dense"
      label="Search"
      size="small"
      value={searchKey}
      onChange={(e) => setSearchKey(e.target.value)}
      sx={{
        mt: 3,
        ml: "38%",
        width: 370,

        "& .MuiOutlinedInput-root": {
          borderRadius: "37px",

          "& fieldset": {
            borderColor: "#1976d2",
          },

          "&:hover fieldset": {
            borderColor: "#1565c0",
          },

          "&.Mui-focused fieldset": {
            borderColor: "#0d47a1",
          },
        },
      }}
    />


    <UsersLogsTable
    activeTab={activeTab}
    isLoading={isLoading}
    users={users}
    handleOpenRoleDialog={handleOpenRoleDialog}
    handleDeleteUser={handleDeleteUser}
    deleteUserMutation={deleteUserMutation}
    logsLoading={logsLoading}
    logs={logs}
    />

    <ChangeRoleDialog
        openRoleDialog={openRoleDialog}
        handleClose={handleClose}
        setOpenRoleDialog={setOpenRoleDialog}
        newRole={newRole}
        handleUpdateRole={handleUpdateRole}
        setNewRole={setNewRole}
        updateRoleMutation={updateRoleMutation}
    />

        <Box sx={{ display: "flex", justifyContent: "center", mt: 2, gap: 2 }}>
        <PaggingUserLog
        setPage={setPage}
        page={page}
        totalPages={totalPages}
        />
       </Box>


        <Toast
            toast={toast}
            setToast={setToast}
        />

        <DeleteUserDialog
        openDeleteDialog={openDeleteDialog}
        setOpenDeleteDialog={setOpenDeleteDialog}
        confirmDeleteUser={confirmDeleteUser}
        deleteUserMutation={deleteUserMutation}
        />
    </Box>
  );
}

export default UserManagment;
