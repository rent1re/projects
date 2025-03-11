using System;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace C#
{
    public class NewClass
    {
        // Свойства
        public int Id { get; set; }
        public string Name { get; set; }

        // Конструктор
        public NewClass(int id, string name)
        {
            Id = id;
            Name = name;
        }

        // Метод
        public void PrintDetails()
        {
            Console.WriteLine($"Id: {Id}, Name: {Name}");
        }
    }
}