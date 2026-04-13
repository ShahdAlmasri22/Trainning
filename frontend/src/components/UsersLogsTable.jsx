import {
    Box,
    Button,
    CircularProgress,
    Paper,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow
} from "@mui/material";


export default function UsersLogsTable(
    {
        activeTab,
        isLoading,
        users,
        handleOpenRoleDialog,
        handleDeleteUser,
        deleteUserMutation,
        logsLoading,
        logs,
    }
  ){

    return(
        <Box>
            <TableContainer
        component={Paper}
        sx={{
          mt: 4,
          width: "80%",
          borderRadius: 3,
          mx: "auto",
          background: "#dbdffd",
        }}
      >
        <Table size="small">

          {activeTab === "users" && (
            <>
              <TableHead>
                <TableRow
                  sx={{
                    background: "linear-gradient(135deg, #7e92e1, #8f6eac)",
                  }}
                >
                  <TableCell sx={{ color: "white" }}><b>ID</b></TableCell>
                  <TableCell sx={{ color: "white" }}><b>Name</b></TableCell>
                  <TableCell sx={{ color: "white" }}><b>Email</b></TableCell>
                  <TableCell sx={{ color: "white" }}><b>Role</b></TableCell>
                  <TableCell sx={{ color: "white" }}><b>Actions</b></TableCell>
                </TableRow>
              </TableHead>

              <TableBody>
                {isLoading ? (
                  <TableRow>
                    <TableCell colSpan={5} align="center">
                      <Box
                        sx={{
                          display: "flex",
                          justifyContent: "center",
                          alignItems: "center",
                          py: 3,
                        }}
                      >
                        <CircularProgress />
                      </Box>
                    </TableCell>
                  </TableRow>
                ) : (
                  users.map((user) => (
                    <TableRow
                      key={user.ID}
                      sx={{
                        borderBottom: "1px solid #cfcfcf",
                      }}
                    >
                      <TableCell>{user.ID}</TableCell>
                      <TableCell>{user.name}</TableCell>
                      <TableCell>{user.email}</TableCell>
                      <TableCell>{user.role}</TableCell>
                      <TableCell>
                        <Button
                          size="small"
                          sx={{
                            borderRadius: 3,
                            fontSize: "10px",
                            background: "#8f6eac",
                            color: "white",
                            mr: 1,
                            px:2.5,
                            py:0.3,
                            ml:6
                          }}
                          onClick={() => handleOpenRoleDialog(user)}
                        >
                          Change Role
                        </Button>

                        <Button
                          size="small"
                          sx={{
                            borderRadius: 3,
                            fontSize: "10px",
                            background: "#dc322c",
                            color: "white",
                            px:2.5,
                            py:0.3
                          }}
                          onClick={() => handleDeleteUser(user.ID)}
                          disabled={deleteUserMutation.isPending}
                        >
                          {deleteUserMutation.isPending ? "Deleting..." : "Delete"}
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </>
          )}

          {activeTab === "logs" && (
            <>
              <TableHead>
                <TableRow
                  sx={{
                    background: "linear-gradient(135deg, #7e92e1, #8f6eac)",
                  }}
                >
                  <TableCell sx={{ color: "white" }}><b>ID</b></TableCell>
                  <TableCell sx={{ color: "white" }}><b>Method</b></TableCell>
                  <TableCell sx={{ color: "white" }}><b>Path</b></TableCell>
                  <TableCell sx={{ color: "white" }}><b>Status</b></TableCell>
                  <TableCell sx={{ color: "white" }}><b>User</b></TableCell>
                  <TableCell sx={{ color: "white" }}><b>Date</b></TableCell>
                </TableRow>
              </TableHead>

              <TableBody>
                {logsLoading ? (
                  <TableRow>
                    <TableCell colSpan={6} align="center">
                      <Box
                        sx={{
                          display: "flex",
                          justifyContent: "center",
                          alignItems: "center",
                          py: 3,
                        }}
                      >
                        <CircularProgress />
                      </Box>
                    </TableCell>
                  </TableRow>
                ) : (
                  logs.map((log) => (
                    <TableRow
                      key={log.id}
                      sx={{ borderBottom: "1px solid #cfcfcf" }}
                    >
                      <TableCell>{log.id}</TableCell>
                      <TableCell>{log.method}</TableCell>
                      <TableCell>{log.path}</TableCell>
                      <TableCell>{log.status}</TableCell>
                      <TableCell>{log.user}</TableCell>
                      <TableCell>{log.date}</TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </>
          )}

        </Table>
      </TableContainer>
        </Box>
    );
}
