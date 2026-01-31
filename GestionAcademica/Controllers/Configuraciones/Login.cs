using Microsoft.AspNetCore.Mvc;

namespace GestionAcademica.Controllers.Configuraciones
{
    public class Login : Controller
    {
        public IActionResult Index()
        {
            return View();
        }
    }
}
