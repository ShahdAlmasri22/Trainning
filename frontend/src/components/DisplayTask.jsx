import {Box, Button, Card, CircularProgress, Typography} from "@mui/material";


export default function DisplayTask(
    {
        isNoTasksAtAll,
        setOpen,
        isNoSearchResults,
        searchKey,
        data,
        isInitialLoading,
        handleOpenEdit,
        setTaskToDelete,
        setDeleteOpen,
        formatDate
    }
){
    return(
        <>
        <Box
          sx={{
            p: 3,
            display: "grid",
            gridTemplateColumns: "repeat(auto-fill,minmax(260px,1fr))",
            gap: 1.5,
          }}
        >

          {isNoTasksAtAll ? (
        <Box sx={{ textAlign: "center", mt: 8, gridColumn: "1 / -1", alignItems: "center", display: "flex", flexDirection: "column", justifyContent: "center",}}>
        <Typography sx={{ fontSize: "22px", fontWeight: "bold", color: "#5b3180"}}>
          No tasks yet. Create one!
        </Typography>

        <Typography sx={{ color: "#666" }}>
          Start by creating your first task
        </Typography>

        <Button
          onClick={() => setOpen(true)}
          sx={{
            textTransform: "none",
            background: "#8b8fc3",
            p: 1.2,
            borderRadius: 4,
            color: "white",
            boxShadow: 4,
            mt: 2,
          }}
        >
          Create Task +
        </Button>
        </Box>

        )  : isNoSearchResults ? (
          <Box sx={{ textAlign: "center", mt: 8, gridColumn: "1 / -1" }}>
            No tasks found for "{searchKey}" 🔍
          </Box> ):
              data?.tasks.length === 0 ? (
          <Box
            sx={{
              textAlign: "center",
              width: "100%",
              color: "#555",
              fontSize: "14px",
            }}
          >
            No tasks found...
          </Box>
        ) : isInitialLoading ? (
        <Box
          sx={{
            gridColumn: "1 / -1",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            mt: 5,
          }}
        >
        <CircularProgress />
        </Box>
        ) : (data?.tasks?.map((task) => (
            <Card
              key={task.task_id}
              sx={{
                p: 2,
                borderRadius: 3,
                color: "white",
                background: "linear-gradient(135deg, #7e92e1, #8f6eac)",
                display: "flex",
                flexDirection: "column",
                gap: 1,
                mt: 3,
              }}
            >
              <Typography fontWeight="bold" fontSize="23px" >
                {task.title}
              </Typography>

              <Typography fontSize="18px" sx={{ opacity: 0.9 }}>
                {task.description}
              </Typography>

              <Box sx={{ fontSize: "10px", opacity: 0.9 }}>
                <Typography sx={{fontSize: "13px"}}>Priority: {task.priority}</Typography>
                <Typography sx={{fontSize: "13px"}}>Status: {task.status}</Typography>
                <Typography sx={{fontSize: "13px"}}>Created: {formatDate(task.created_at)}</Typography>
                <Typography sx={{fontSize: "13px"}}>Updated: {formatDate(task.updated_at)}</Typography>
              </Box>

              <Box
                sx={{
                  display: "flex",
                  flexDirection: "column",
                  gap: 1.5,
                  mt: 1,
                }}
              >
                <Button
                  size="small"
                  variant="contained"
                  sx={{
                    fontSize: "11px",
                    padding: "4px 8px",
                    minWidth: "unset",
                    backgroundColor: "#ffffff30",
                    borderRadius: 3,
                    "&:hover": { backgroundColor: "#ffffff50" },
                  }}
                  onClick={() => handleOpenEdit(task)}
                >
                  Update
                </Button>

                <Button
                  size="small"
                  color="error"
                  variant="contained"
                  sx={{
                    fontSize: "11px",
                    padding: "4px 8px",
                    minWidth: "unset",
                    borderRadius: 3,
                  }}
                  onClick={() => {
                  setTaskToDelete(task.task_id);
                  setDeleteOpen(true);
                }}
                >
                  Delete
                </Button>
              </Box>
            </Card>
          )))}
        </Box>
        </>
    );
}
