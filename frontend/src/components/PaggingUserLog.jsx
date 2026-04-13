import {Box, Button, Typography} from "@mui/material";


export default function PaggingUserLog(
    {
        setPage,
        page,
        totalPages,
    }
){
    return(
        <>
              <Button
                variant="contained"
                disabled={page === 1}
                onClick={() => setPage((prev) => prev - 1)}
                sx={{
                  textTransform: "none",
                  borderRadius: 3,
                  px:2.5,
                  py:0.5,
                  fontSize: "12px"
                }}
              >
                ← Previous
              </Button>

        <Typography sx={{fontSize: "14px", mt:0.5}}>
          Page {page} / {totalPages || 1}
        </Typography>

        <Button
          variant="contained"
          disabled={page === totalPages}
          onClick={() => setPage((prev) => prev + 1)}
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
     </>
    );
}
