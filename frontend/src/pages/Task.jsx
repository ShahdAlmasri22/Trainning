import { useState, useEffect } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  Box,
  Typography,
  Button,
  TextField,
  MenuItem, Select, FormControl, InputLabel,
} from "@mui/material";
import EditTaskDialog from "../components/EditTaskDialog";
import DeleteTaskDialog from "../components/DeleteTaskDialog";
import { useNavigate } from "react-router-dom";
import EditProfileDialog from "../components/EditProfileDialog.jsx";
import DeleteAccountDialog from "../components/DeleteAccountDialog.jsx";
import AddNewTaskDialog from "../components/AddNewTaskDialog.jsx";
import Sorting from "../components/Sorting.jsx";
import Filtering from "../components/Filtering.jsx";
import Toast from "../components/Toast.jsx";
import DisplayTask from "../components/DisplayTask.jsx";
import DeleteAllTask from "../components/DeleteAllTask.jsx";

export default function Task() {
  const baseURL = import.meta.env.VITE_BACK_URL;
  const queryClient = useQueryClient();
  const [openMenu, setOpenMenu] = useState(false);

  const [editOpen, setEditOpen] = useState(false);
  const [selectedTask, setSelectedTask] = useState(null);
  const [editTitle, setEditTitle] = useState("");
  const [editDesc, setEditDesc] = useState("");
  const [editPriority, setEditPriority] = useState("LOW");
  const [editStatus, setEditStatus] = useState("PENDING");

  const [deleteOpen, setDeleteOpen] = useState(false);
  const [taskToDelete, setTaskToDelete] = useState(null);

  const [open, setOpen] = useState(false);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [priority, setPriority] = useState("LOW");

  const [sortBy, setSortBy] = useState("created_at");
  const [order, setOrder] = useState("desc");

  const [limit, setLimit] = useState(10);
  const [skip, setSkip] = useState(0);

  const [filterPriority, setFilterPriority] = useState("");
  const [filterStatus, setFilterStatus] = useState("");

  const [searchKey, setSearchKey] = useState("");
  const [debouncedSearch, setDebouncedSearch] = useState("");

  const [deleteAcc, setDeleteAcc] = useState(false);

  const [openDeleteAll, setOpenDeleteAll] = useState(false);
  const [openProfile, setOpenProfile] = useState(false);

  const [profileData, setProfileData] = useState({
      name: "",
      oldPassword: "",
      newPassword: "",
  });

  const Role = localStorage.getItem("role");

  const navigate = useNavigate();

  const [toast, setToast] = useState({
    open: false,
    message: "",
    severity:  "error" | "success" | "warning" | "info",
  });

  const toastSuccess = (msg) =>
  setToast({ open: true, message: msg, severity: "success" });

  const toastError = (msg) =>
  setToast({ open: true, message: msg, severity: "error" });



  const healthQuery = useQuery({
    queryKey: ["health"],
    queryFn: async () => {
      return fetchWithAuth(`${baseURL}/health`);
    },
    retry: false,
  });

  useEffect(() => {
    if (healthQuery.isError) {
      toastError(healthQuery.error.message || "Server error ❌", "error");
    }
  }, [healthQuery.isError]);


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

  const { data, isLoading, isError } = useQuery({
    queryKey: ["tasks",sortBy, order, limit, skip, filterPriority, filterStatus, debouncedSearch],
    queryFn: () => {
      let url = `${baseURL}/tasks/view`;

       const search = debouncedSearch?.trim();

       if (search) {
        url = `${baseURL}/tasks/search?key=${search}`;}

      else if(!filterPriority && !filterStatus) {
         url = `${baseURL}/tasks/filter?sort_by=${sortBy}&order=${order}&skip=${skip}&limit=${limit}`;
      }


      else {
        url =`${baseURL}/tasks/prio_stat?`;
        if (filterPriority) {
            url += `priority=${filterPriority}`;
        }

        if (filterStatus) {
            url += `&status=${filterStatus}`;
        }
    }

      return fetchWithAuth(url);
    },
    onError: (err) => {
    toastError(err.message);
    },
      keepPreviousData: true,
  });


  const createTaskMutation = useMutation({
    mutationFn: async (newTask) => {
      return fetchWithAuth(`${baseURL}/tasks`, {
        method: "POST",
        body: JSON.stringify(newTask),
      });

    },
      onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["tasks"] });
      setOpen(false);

      setTitle("");
      setDescription("");
      setPriority("");

      toastSuccess("Task created successfully ✅");
      },
    onError: (err) => {
      toastError(err.message);
    },
  });

  function formatDate(dateString){
    const date = new Date(dateString);

    return date.toLocaleString("en-GB", {
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit"
    });
  }

  const confirmDeleteAll = () => {
    deleteAllMutation.mutate();
    setOpenDeleteAll(false);
  };

  const updateProfileMutation = useMutation({
    mutationFn: async (body) => {
    const user_id = localStorage.getItem("user_id");

    return fetchWithAuth(`${baseURL}/users/profile/${user_id}`, {
      method: "PATCH",
      body: JSON.stringify(body),
    });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["tasks"] });
      setOpenProfile(false);
      setProfileData({ name: "", oldPassword: "", newPassword: "" });
      toastSuccess("Profile updated successfully ✏️");
    },

    onError: (err) => {
      toastError(err.message);
    },
  });


  const deleteTaskMutation = useMutation({
    mutationFn: async (id) => {
      return fetchWithAuth(`${baseURL}/tasks/${id}`, {
        method: "DELETE",
      });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["tasks"] });
      toastSuccess("Task deleted 🗑️");
      },
      onError: (err) => {
        toastError(err.message);
      },
  });


  const updateTaskMutation = useMutation({
    mutationFn: async ({ id, data }) => {
      return fetchWithAuth(`${baseURL}/tasks/${id}`, {
        method: "PATCH",
        body: JSON.stringify(data),
      });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["tasks"] });
      setEditOpen(false);
      toastSuccess("Task updated successfully ✏️");
    },
    onError: (err) => {
      toastError(err.message);
    },
  });


  const handleOpenEdit = (task) => {
    setSelectedTask(task);
    setEditTitle(task.title);
    setEditDesc(task.description);
    setEditPriority(task.priority);
    setEditStatus(task.status);
    setEditOpen(true);
  };

  const handleUpdate = () => {
    updateTaskMutation.mutate({
      id: selectedTask.task_id,
      data: {
        title: editTitle,
        description: editDesc,
        priority: editPriority,
        status: editStatus,
      },
    });
  };


  const handleDelete = () => {
    deleteTaskMutation.mutate(taskToDelete);
    setDeleteOpen(false);
    setTaskToDelete(null);
  };

  const deleteAllMutation = useMutation({
    mutationFn: async () => {
      return fetchWithAuth(`${baseURL}/tasks/all`, {
        method: "DELETE",
      });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["tasks"] });
      toastSuccess("All tasks deleted 🧹");
    },
    onError: (err) => {
      toastError(err.message);
    },
  });


  const deleteAccountMutation = useMutation({
     mutationFn: async () => {
      const user_id = localStorage.getItem("user_id");

      return fetchWithAuth(`${baseURL}/users/${user_id}`, {
        method: "DELETE",
      });
    },

    onSuccess: () => {
      localStorage.clear();

      queryClient.clear();
      toastSuccess("Account deleted successfully");
      window.location.href = "/users/login";
    },

    onError: (err) => {
      toastError(err.message);
    },
  });



  const handleLogout = () => {
    localStorage.clear();
    toastSuccess("Logged out 👋");
    setTimeout(() => {
    window.location.href = "/users/login";
    }, 500);
  };

  const handleProfile = () => {
    if( Role === "ADMIN") {
      navigate("/UserManagment")
    }
    else{
      return alert("You don't have permission.")
    }
  };


  useEffect(() => {
    const handleClickOutside = () => setOpenMenu(false);
    if (openMenu) window.addEventListener("click", handleClickOutside);

    return () =>
      window.removeEventListener("click", handleClickOutside);
  }, [openMenu]);

    useEffect(() => {
        setDebouncedSearch(searchKey);
    }, [searchKey]);



  const tasks = data?.tasks ?? [];
  const totalTasks = data?.total_tasks;

  const isAdmin = Role === "ADMIN" ? true : false;
  const isNoTasksAtAll = !isLoading && totalTasks === 0;

  const isSearching = searchKey.trim() !== "";

  const isNoSearchResults = isSearching && !isLoading && tasks.length === 0;

  const isInitialLoading = isLoading && !data;

  if (isError) return <p>Error loading tasks</p>;

  return (
  <Box sx={{overflowX: "hidden"}}>
        <Typography
          sx={{
            textAlign: "center",
            mt: 3,
            fontWeight: "bold",
            fontSize: "28px",
            color: "#472661"
          }}
        >
        My Tasks
        </Typography>

        <Box
          sx={{
            ml: 3
          }}
        >
        <img
          src="/images/profile.png"
          alt="profile"
          onClick={(e) => {
            e.stopPropagation();
            setOpenMenu(!openMenu);
          }}
          style={{
            width: "35px",
            height: "35px",
            cursor: "pointer",
          }}
        />
        {openMenu && (
    <Box
      sx={{
        position: "absolute",
        mt: 0.5,
        ml: 0.2,
        background: "white",
        borderRadius: 2,
        boxShadow: 3,
        p: 1,
        width: 180,
        zIndex: 500,
        color: "#4e57a8"
      }}
    >
      {isAdmin && (
      <Button sx={{textTransform: "none"}} fullWidth size="small" onClick={handleProfile} >User management</Button>
      )}
      <Button sx={{textTransform: "none"}} fullWidth size="small" onClick={() => setOpenProfile(true)}>Edit Profile</Button>
      <Button sx={{textTransform: "none"}} fullWidth size="small" color="error" onClick={() => setDeleteAcc(true)}>Delete Account</Button>
      <Button sx={{textTransform: "none"}} fullWidth size="small" onClick={handleLogout}>Log Out</Button>
    </Box>
    )}
    </Box>

    <EditProfileDialog
        openProfile={openProfile}
        setOpenProfile={setOpenProfile}
        profileData={profileData}
        setProfileData={setProfileData}
        updateProfileMutation={updateProfileMutation}
    />

    <DeleteAccountDialog
        deleteAcc={deleteAcc}
        setDeleteAcc={setDeleteAcc}
        deleteAccountMutation={deleteAccountMutation}
    />

    <Button sx={{
        textTransform: "none",
        background: "#8b8fc3",
        ml: 4,
        mt:2,
        p:1.2,
        borderRadius: 4,
        color: "white",
        boxShadow: 4
    }}  size="small"
    onClick={() => setOpen(true)}
    >
        Add new task +
    </Button>

    <AddNewTaskDialog
        open={open}
        setOpen={setOpen}
        title={title}
        setTitle={setTitle}
        description={description}
        setDescription={setDescription}
        priority={priority}
        setPriority={setPriority}
        createTaskMutation={createTaskMutation}
    />

    <Button sx={{
      textTransform: "none",
      background: "#702424",
      ml: 2,
      mt: 2,
      p: 1.2,
      borderRadius: 4,
      color: "white",
      boxShadow: 4
      }}  size="small"
      onClick={() => setOpenDeleteAll(true)}
      disabled={deleteAllMutation.isPending}
      >
      {deleteAllMutation.isPending ? "Deleting..." : "Delete all tasks"}
    </Button>


    <Sorting
        sortBy={sortBy}
        setSortBy={setSortBy}
        order={order}
        setOrder={setOrder}
    />

    <Box
      sx={{
        display: "flex",
        alignItems: "center",
        gap: 1.5,
        mt: 3,
        ml: 4,
        flexWrap: "wrap",
      }}
    >
    <FormControl
      size="small"
      sx={{
        minWidth: 80,
        borderRadius: 3,
        boxShadow: 3,
      }}
    >
    <InputLabel>Show</InputLabel>
    <Select
      value={limit}
      label="Show"
      onChange={(e) => {
        setLimit(Number(e.target.value));
        setSkip(0);
      }}
      sx={{
        borderRadius: 3,
        "& .MuiSelect-icon": { },
      }}
    >
      <MenuItem value={5}>5</MenuItem>
      <MenuItem value={8}>8</MenuItem>
      <MenuItem value={10}>10</MenuItem>
      <MenuItem value={15}>15</MenuItem>
      <MenuItem value={20}>20</MenuItem>
    </Select>
    </FormControl>

    <Typography
      sx={{
        fontSize: "16px",
        fontWeight: 500,
        color: "black",
      }}
    >
    tasks per page,
    </Typography>

    <FormControl
      size="small"
      sx={{
        minWidth: 80,
        borderRadius: 3,
        boxShadow: 3,
      }}
    >
    <InputLabel>Skip</InputLabel>
    <Select
      value={skip}
      label="Skip"
      onChange={(e) => setSkip(Number(e.target.value))}
      sx={{
        borderRadius: 3,
      }}
    >
      <MenuItem value={0}>0</MenuItem>
      <MenuItem value={5}>5</MenuItem>
      <MenuItem value={10}>10</MenuItem>
      <MenuItem value={15}>15</MenuItem>
      <MenuItem value={20}>20</MenuItem>
    </Select>
    </FormControl>

    <Typography
      sx={{
        fontSize: "16px",
        fontWeight: 500,
        color: "black",
      }}
    >
    of tasks
    </Typography>
    </Box>



    <Box
      sx={{
        display: "flex",
        alignItems: "center",
        gap: 1.5,
        mt: 3,
        ml: 4,
        flexWrap: "wrap",
      }}
    >

      <Filtering
       filterPriority={filterPriority}
       setFilterPriority={setFilterPriority}
       setSkip={setSkip}
       filterStatus={filterStatus}
       setFilterStatus={setFilterStatus}
      />


   <TextField
    margin="dense"
    label="Search"
    size="small"
    value={searchKey}
    onChange={(e) => {
        setSearchKey(e.target.value);
      }}
    sx={{
      mb: 1,
      ml: 17,
      width: 350,

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
    </Box>


    <Box
      sx={{
        display: "flex",
        justifyContent: "center",
        mt: 2,
      }}
    >
    <Box
        sx={{
          background: "white",
          px: 3,
          py: 1,
          borderRadius: 2,
          boxShadow: 5,
          fontWeight: "bold",
          color: "#5b3180",
        }}
    >
        Total Tasks: {data?.total_tasks}
    </Box>
    </Box>

    <DisplayTask
        isNoTasksAtAll={isNoTasksAtAll}
        setOpen={setOpen}
        isNoSearchResults={isNoSearchResults}
        searchKey={searchKey}
        data={data}
        isInitialLoading={isInitialLoading}
        handleOpenEdit={handleOpenEdit}
        setTaskToDelete={setTaskToDelete}
        setDeleteOpen={setDeleteOpen}
        formatDate={formatDate}
    />

    <EditTaskDialog
      open={editOpen}
      setOpen={setEditOpen}
      editTitle={editTitle}
      setEditTitle={setEditTitle}
      editDesc={editDesc}
      setEditDesc={setEditDesc}
      editPriority={editPriority}
      setEditPriority={setEditPriority}
      editStatus={editStatus}
      setEditStatus={setEditStatus}
      handleUpdate={handleUpdate}
      updateTaskMutation={updateTaskMutation}
    />

    <DeleteTaskDialog
      open={deleteOpen}
      setOpen={setDeleteOpen}
      handleDelete={handleDelete}
      deleteTaskMutation={deleteTaskMutation}
    />

    <DeleteAllTask
        openDeleteAll={openDeleteAll}
        setOpenDeleteAll={setOpenDeleteAll}
        confirmDeleteAll={confirmDeleteAll}
        deleteAllMutation={deleteAllMutation}
    />
  <Box
    sx={{
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      gap: 1.5,
      mt: 2,
      mb:2
    }}
  >
  <Button
    variant="contained"
    disabled={skip === 0}
    onClick={() => setSkip((prev) => Math.max(prev - limit, 0))}
    sx={{
      textTransform: "none",
      borderRadius: 3,
      px:3,
      py:0.5,
      fontSize: "12px"
    }}
  >
    ← Previous
  </Button>

  <Typography sx={{fontSize: "14px"}}>
    Page {Math.floor(skip / limit) + 1}
  </Typography>

  <Button
    variant="contained"
    onClick={() => setSkip((prev) => prev + limit)}
    sx={{
      textTransform: "none",
      borderRadius: 3,
      px:3,
      py:0.5,
      fontSize: "12px"
    }}
  >
    Next →
  </Button>
  </Box>

  <Toast
        toast={toast}
        setToast={setToast}
  />
</ Box>

  );
}

